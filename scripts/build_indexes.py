import os
from backend.api.btree import BPlusTree
import struct

# Defina os campos e tamanhos (deve ser igual ao usado no csv_to_bin.py)
fields = [
    ('data_extracao', 19),
    ('descricao', 40),
    ('estado', 12),
    ('complemento', 100),
    ('implantacao', 10),
    ('logradouro_nome', 40),
    ('num_inicial', 10),
    ('num_final', 10),
    ('defronte', 4),
    ('cruzamento_nome', 40),
    ('lado', 8),
    ('fluxo', 12),
    ('local_de_instal', 30),
    ('latitude', 20),
    ('longitude', 20),
]
record_struct = struct.Struct(' '.join(f'{size}s' for _, size in fields))
record_size = record_struct.size

# Índices para os campos desejados
index_logradouro = BPlusTree(index_file='data/bin/infra_cicloviaria_logradouro.idx')
index_implantacao = BPlusTree(index_file='data/bin/infra_cicloviaria_implantacao.idx')

# Função auxiliar para descobrir o maior offset já indexado
def get_max_offset(index):
    max_offset = -1
    # Percorre todas as folhas e offsets para encontrar o maior
    def _walk(node):
        nonlocal max_offset
        if node.leaf:
            for _, offsets in node.keys:
                if offsets:
                    max_offset = max(max_offset, max(offsets))
        else:
            for child in node.children:
                _walk(child)
    _walk(index.root)
    return max_offset

# Descobre o maior offset já indexado em cada índice
max_offset_logradouro = get_max_offset(index_logradouro)
max_offset_implantacao = get_max_offset(index_implantacao)
# Usa o maior dos dois para garantir que nenhum registro será pulado
last_indexed_offset = max(max_offset_logradouro, max_offset_implantacao, -1)

with open('data/bin/infra_cicloviaria.bin', 'rb') as binfile:
    offset = 0
    while True:
        bytes_read = binfile.read(record_size)
        if not bytes_read or len(bytes_read) < record_size:
            break
        if offset <= last_indexed_offset:
            offset += record_size
            continue  # Pula registros já indexados
        unpacked = record_struct.unpack(bytes_read)
        # Extrai os campos (removendo espaços extras e decodificando)
        implantacao = unpacked[4].decode('utf-8').strip()
        logradouro_nome = unpacked[5].decode('utf-8').strip().upper()
        # Adiciona ao índice
        index_logradouro.insert(logradouro_nome, offset)
        index_implantacao.insert(implantacao, offset)
        offset += record_size

# Salva os índices em disco
index_logradouro.save()
index_implantacao.save()