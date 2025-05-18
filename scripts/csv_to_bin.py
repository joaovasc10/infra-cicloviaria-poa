# Este script lê o arquivo CSV filtrado com dados de infraestrutura cicloviária
# e converte cada linha em um registro binário de tamanho fixo, salvando todos
# os registros no arquivo 'data/bin/infra_cicloviaria.bin'. O objetivo é permitir
# o armazenamento eficiente e estruturado dos dados para posterior indexação, busca e análise.

import csv
import struct
import os

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

os.makedirs('data/bin', exist_ok=True)

with open('data/processed/filtrado_infra_cicloviaria.csv', encoding='utf-8') as csvfile, \
     open('data/bin/infra_cicloviaria.bin', 'wb') as binfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        packed = record_struct.pack(*[
            (row.get(field, '') or '').encode('utf-8')[:size].ljust(size, b' ')
            for field, size in fields
        ])
        binfile.write(packed)