import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .btree import BPlusTree
import struct
from django.conf import settings

# Definição dos campos e tamanhos, igual ao usado nos scripts de geração
fields = [
    ('data_extracao', 19), ('descricao', 40), ('estado', 12), ('complemento', 100),
    ('implantacao', 10), ('logradouro_nome', 40), ('num_inicial', 10), ('num_final', 10),
    ('defronte', 4), ('cruzamento_nome', 40), ('lado', 8), ('fluxo', 12),
    ('local_de_instal', 30), ('latitude', 20), ('longitude', 20),
]
record_struct = struct.Struct(' '.join(f'{size}s' for _, size in fields))
record_size = record_struct.size

def read_records_by_offsets(offsets):
    """
    Lê registros do arquivo binário a partir de uma lista de offsets.
    Retorna uma lista de dicionários com os dados dos registros.
    """
    results = []
    bin_path = os.path.join(settings.BASE_DIR, '..', 'data', 'bin', 'infra_cicloviaria.bin')
    bin_path = os.path.abspath(bin_path)
    with open(bin_path, 'rb') as binfile:
        for offset in offsets:
            binfile.seek(offset)
            data = binfile.read(record_size)
            if len(data) == record_size:
                unpacked = record_struct.unpack(data)
                record = {field: unpacked[i].decode('utf-8').strip() for i, (field, _) in enumerate(fields)}
                results.append(record)
    return results

class BuscaPorLogradouro(APIView):
    """
    Endpoint para buscar registros pelo nome do logradouro.
    Exemplo de uso: GET /api/busca-logradouro/?logradouro_nome=R MARIANTE
    """
    def get(self, request):
        logradouro = request.GET.get('logradouro_nome')
        if not logradouro:
            return Response({'error': 'Parâmetro logradouro_nome é obrigatório.'}, status=400)
        logradouro = logradouro.strip().upper()
        index = BPlusTree(index_file=os.path.join(settings.BASE_DIR, '..', 'data', 'bin', 'infra_cicloviaria_logradouro.idx'))
        offsets = index.search(logradouro)
        results = read_records_by_offsets(offsets)
        return Response(results)

class BuscaPorImplantacao(APIView):
    """
    Endpoint para buscar registros pela data de implantação.
    Exemplo de uso: GET /api/busca-implantacao/?implantacao=2018-06-21
    """
    def get(self, request):
        implantacao = request.GET.get('implantacao')
        if not implantacao:
            return Response({'error': 'Parâmetro implantacao é obrigatório.'}, status=400)
        implantacao = implantacao.strip()
        index = BPlusTree(index_file=os.path.join(settings.BASE_DIR, '..', 'data', 'bin', 'infra_cicloviaria_implantacao.idx'))
        offsets = index.search(implantacao)
        results = read_records_by_offsets(offsets)
        return Response(results)