import pickle
import os
from collections import defaultdict

class BTreeIndex:
    """
    Estrutura de índice simples baseada em dicionário para mapear chaves (ex: logradouro_nome ou implantacao)
    para offsets no arquivo binário. O índice é persistido em disco usando pickle.
    """

    def __init__(self, index_file):
        """
        Inicializa o índice.
        - index_file: caminho do arquivo onde o índice será salvo/carregado.
        """
        self.index_file = index_file
        # defaultdict(list): cada chave pode ter múltiplos offsets (caso haja mais de um registro com o mesmo valor)
        self.index = defaultdict(list)
        # Se o arquivo de índice já existe, carrega o índice do disco
        if os.path.exists(self.index_file):
            self.load()

    def add(self, key, offset):
        """
        Adiciona um novo offset para a chave informada.
        - key: valor do campo indexado (ex: nome da rua ou data de implantação)
        - offset: posição do registro no arquivo binário
        """
        self.index[key].append(offset)

    def get(self, key):
        """
        Retorna a lista de offsets associados à chave informada.
        - key: valor do campo indexado
        """
        return self.index.get(key, [])

    def save(self):
        """
        Salva o índice no disco usando pickle.
        """
        with open(self.index_file, 'wb') as f:
            pickle.dump(dict(self.index), f)

    def load(self):
        """
        Carrega o índice do disco.
        """
        with open(self.index_file, 'rb') as f:
            self.index = defaultdict(list, pickle.load(f))

    def keys(self):
        """
        Retorna todas as chaves indexadas, ordenadas.
        """
        return sorted(self.index.keys())