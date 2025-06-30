import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .btree import BPlusTree
import struct
from django.conf import settings
from silk.profiling.profiler import silk_profile

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
            if len(data) != record_size:
                continue
            unpacked = record_struct.unpack(data)
            record = {
                field: unpacked[i].decode('utf-8').rstrip('\x00').strip()
                for i, (field, _) in enumerate(fields)
            }
            results.append(record)
    return results

class BuscaPorLogradouro(APIView):
    """
    Endpoint para buscar registros pelo nome do logradouro.
    Exemplo de uso: GET /api/busca-logradouro/?logradouro_nome=R MARIANTE
    """
    @silk_profile(name='view_get_busca_logradouro')
    def get(self, request):
        logradouro = request.GET.get('logradouro_nome')
        if not logradouro:
            return Response(
                {'error': 'Parâmetro logradouro_nome é obrigatório.'}, 
                status=400
            )
        logradouro = logradouro.strip().upper()
        with silk_profile(name='btree_search'):
            index = BPlusTree(index_file=os.path.join(settings.BASE_DIR, '..', 'data', 'bin', 'infra_cicloviaria_logradouro.idx'))
            offsets = index.search(logradouro)
        
        # Paginação
        page = int(request.GET.get('page', 1))
        pagesize = int(request.GET.get('pagesize', 10))
        start = (page - 1) * pagesize
        end = start + pagesize
        paged_offsets = offsets[start:end]

        results = read_records_by_offsets(paged_offsets)

        # Normaliza campos e converte latitude/longitude
        for rec in results:
            for k, v in rec.items():
                if k in ('latitude', 'longitude'):
                    clean = v  # já sem '\x00', pois read_records_by_offsets faz rstrip
                    rec[k] = float(clean) if clean else None
                else:
                    rec[k] = v

        return Response({
            'page': page,
            'pagesize': pagesize,
            'total': len(offsets),
            'results': results
        })

class BuscaPorImplantacao(APIView):
    """
    Endpoint para buscar registros pela data de implantação.
    Exemplo de uso: GET /api/busca-implantacao/?implantacao=2018-06-21
    """
    @silk_profile(name='view_get_busca_implantacao')
    def get(self, request):
        implantacao = request.GET.get('implantacao')
        if not implantacao:
            return Response({'error': 'Parâmetro implantacao é obrigatório.'}, status=400)
        implantacao = implantacao.strip()
        index = BPlusTree(index_file=os.path.join(settings.BASE_DIR, '..', 'data', 'bin', 'infra_cicloviaria_implantacao.idx'))
        offsets = index.search(implantacao)
        
        # Paginação
        page = int(request.GET.get('page', 1))
        pagesize = int(request.GET.get('pagesize', 10))
        start = (page - 1) * pagesize
        end = start + pagesize
        paged_offsets = offsets[start:end]

        results = read_records_by_offsets(paged_offsets)

        for rec in results:
            rec.pop('latitude', None)
            rec.pop('longitude', None)

        return Response({
            'page': page,
            'pagesize': pagesize,
            'total': len(offsets),
            'results': results
        })