import os
from backend.api.btree import BTreeIndex
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
index_logradouro = BTreeIndex('data/bin/infra_cicloviaria_logradouro.idx')
index_implantacao = BTreeIndex('data/bin/infra_cicloviaria_implantacao.idx')

with open('data/bin/infra_cicloviaria.bin', 'rb') as binfile:
    offset = 0
    while True:
        bytes_read = binfile.read(record_size)
        if not bytes_read or len(bytes_read) < record_size:
            break
        unpacked = record_struct.unpack(bytes_read)
        # Extrai os campos (removendo espaços extras e decodificando)
        implantacao = unpacked[4].decode('utf-8').strip()
        logradouro_nome = unpacked[5].decode('utf-8').strip().upper()
        # Adiciona ao índice
        index_logradouro.add(logradouro_nome, offset)
        index_implantacao.add(implantacao, offset)
        offset += record_size

# Salva os índices em disco
index_logradouro.save()
index_implantacao.save()