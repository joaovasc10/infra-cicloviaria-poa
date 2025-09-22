import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import Ciclovia
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa dados de ciclovias a partir de um arquivo CSV para o banco de dados.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando importação de dados...'))

        # Caminho para o arquivo CSV
        csv_path = Path(settings.BASE_DIR).parent / 'data' / 'processed' / 'filtrado_infra_cicloviaria.csv'

        # Limpar dados existentes
        self.stdout.write('Limpando dados antigos...')
        Ciclovia.objects.all().delete()

        ciclovias_a_criar = []
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                # Tratamento de dados antes de criar o objeto
                implantacao_date = None
                if row.get('implantacao'):
                    try:
                        implantacao_date = datetime.strptime(row['implantacao'], '%Y-%m-%d').date()
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Formato de data inválido para implantação: {row['implantacao']}"))

                data_extracao_dt = None
                if row.get('data_extracao'):
                    try:
                        # O formato no CSV é '2025-05-01 01:32:35.866'
                        data_extracao_dt = datetime.fromisoformat(row['data_extracao'])
                    except ValueError:
                         self.stdout.write(self.style.WARNING(f"Formato de data inválido para data_extracao: {row['data_extracao']}"))

                ciclovia = Ciclovia(
                    data_extracao=data_extracao_dt,
                    descricao=row.get('descricao', ''),
                    estado=row.get('estado', ''),
                    complemento=row.get('complemento'),
                    implantacao=implantacao_date,
                    logradouro_nome=row.get('logradouro_nome', '').upper(),
                    num_inicial=row.get('num_inicial'),
                    num_final=row.get('num_final'),
                    defronte=row.get('defronte'),
                    cruzamento_nome=row.get('cruzamento_nome'),
                    lado=row.get('lado'),
                    fluxo=row.get('fluxo'),
                    local_de_instal=row.get('local_de_instal'),
                    latitude=float(row['latitude']) if row.get('latitude') else None,
                    longitude=float(row['longitude']) if row.get('longitude') else None,
                )
                ciclovias_a_criar.append(ciclovia)

        # Inserir em lote
        if ciclovias_a_criar:
            self.stdout.write(f'Inserindo {len(ciclovias_a_criar)} novos registros...')
            Ciclovia.objects.bulk_create(ciclovias_a_criar)

        self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))
