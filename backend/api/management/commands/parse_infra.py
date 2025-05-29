import os
import csv
import struct
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from api.btree import BPlusTree

class Command(BaseCommand):
    help = "Converte CSV filtrado em binário e (re)gera índices B+ para logradouro e implantação."

    def handle(self, *args, **options):
        # 1. Definir paths
        PROJECT_ROOT = Path(settings.BASE_DIR).parent
        RAW_CSV   = PROJECT_ROOT / 'data' / 'processed' / 'filtrado_infra_cicloviaria.csv'
        BIN_DIR   = PROJECT_ROOT / 'data' / 'bin'
        BIN_FILE  = BIN_DIR / 'infra_cicloviaria.bin'
        IDX_LOG   = BIN_DIR / 'infra_cicloviaria_logradouro.idx'
        IDX_IMPL  = BIN_DIR / 'infra_cicloviaria_implantacao.idx'

        # 2. Criar pasta bin se não existir
        BIN_DIR.mkdir(parents=True, exist_ok=True)

        # 3. Definir formato de registro (mesmo tamanho de csv_to_bin.py)
        fields = [
            ('data_extracao', 19), ('descricao', 40), ('estado', 12),
            ('complemento', 100), ('implantacao', 10), ('logradouro_nome', 40),
            ('num_inicial', 10), ('num_final', 10), ('defronte', 4),
            ('cruzamento_nome', 40), ('lado', 8), ('fluxo', 12),
            ('local_de_instal', 30), ('latitude', 20), ('longitude', 20),
        ]
        record_struct = struct.Struct(' '.join(f'{size}s' for _, size in fields))
        record_size = record_struct.size

        # 4. Gerar o arquivo binário
        with open(RAW_CSV, newline='', encoding='utf-8') as csvfile, \
             open(BIN_FILE, 'wb') as binf:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                packed = record_struct.pack(
                    row['data_extracao'].encode()[:19],
                    row['descricao'].encode()[:40],
                    row['estado'].encode()[:12],
                    row['complemento'].encode()[:100],
                    row['implantacao'].encode()[:10],
                    row['logradouro_nome'].encode()[:40],
                    row['num_inicial'].encode()[:10],
                    row['num_final'].encode()[:10],
                    row['defronte'].encode()[:4],
                    row['cruzamento_nome'].encode()[:40],
                    row['lado'].encode()[:8],
                    row['fluxo'].encode()[:12],
                    row['local_de_instal'].encode()[:30],
                    row['latitude'].encode()[:20],
                    row['longitude'].encode()[:20],
                )
                binf.write(packed)

        # 5. Instanciar índices B+ (carrega se já existir)
        index_log = BPlusTree(order=8, index_file=str(IDX_LOG))
        index_imp = BPlusTree(order=8, index_file=str(IDX_IMPL))

        # 6. Função para descobrir último offset indexado
        def get_max_offset(tree: BPlusTree) -> int:
            max_off = -1
            for key in tree.keys():
                for off in tree.search(key):
                    if off > max_off:
                        max_off = off
            return max_off

        last_off_log = get_max_offset(index_log)
        last_off_imp = get_max_offset(index_imp)
        last_indexed = max(last_off_log, last_off_imp, -1)

        # 7. Acrescentar novos registros ao índice
        with open(BIN_FILE, 'rb') as binf:
            offset = 0
            while True:
                chunk = binf.read(record_size)
                if not chunk or len(chunk) < record_size:
                    break
                if offset <= last_indexed:
                    offset += record_size
                    continue
                rec = record_struct.unpack(chunk)
                implant = rec[4].decode('utf-8').rstrip('\x00').strip()
                lograd = rec[5].decode('utf-8').rstrip('\x00').strip().upper()
                index_log.insert(lograd, offset)
                index_imp.insert(implant, offset)
                offset += record_size

        # 8. Salvar índices em disco
        index_log.save()
        index_imp.save()

        self.stdout.write(self.style.SUCCESS(
            f'Binário e índices gerados em {BIN_DIR}'
        ))