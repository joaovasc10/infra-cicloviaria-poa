import pickle
import os

class BPlusTreeNode:
    """
    Nó da árvore B+.
    """
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.next = None

class BPlusTree:
    """
    Implementação básica de uma árvore B+ para indexação de chaves e offsets.
    """
    def __init__(self, order=8, index_file=None):
        self.root = BPlusTreeNode(leaf=True)
        self.order = order
        self.index_file = index_file
        if index_file and os.path.exists(index_file):
            self.load()

    def insert(self, key, offset):
        """
        Insere uma chave e offset na árvore.
        """
        root = self.root
        if len(root.keys) == (self.order - 1):
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, offset)

    def _insert_non_full(self, node, key, offset):
        if node.leaf:
            # Se a chave já existe, adiciona o offset à lista
            for i, (k, offsets) in enumerate(node.keys):
                if k == key:
                    offsets.append(offset)
                    return
            # Caso contrário, insere ordenado
            node.keys.append((key, [offset]))
            node.keys.sort(key=lambda x: x[0])
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1
            child = node.children[i]
            if len(child.keys) == (self.order - 1):
                self._split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1
            self._insert_non_full(node.children[i], key, offset)

    def _split_child(self, parent, index):
        order = self.order
        node = parent.children[index]
        new_node = BPlusTreeNode(leaf=node.leaf)
        mid = order // 2

        if node.leaf:
            # Divide as chaves
            new_node.keys = node.keys[mid:]
            node.keys = node.keys[:mid]
            # Atualiza ponteiros next para manter folhas encadeadas
            new_node.next = node.next
            node.next = new_node
            # Insere referência no pai
            parent.keys.insert(index, new_node.keys[0])
            parent.children.insert(index + 1, new_node)
        else:
            # Divide chaves e filhos para nós internos
            parent.keys.insert(index, node.keys[mid])
            new_node.keys = node.keys[mid + 1:]
            node.keys = node.keys[:mid]
            new_node.children = node.children[mid + 1:]
            node.children = node.children[:mid + 1]
            parent.children.insert(index + 1, new_node)

    def search(self, key):
        """
        Busca offsets associados à chave.
        """
        key = key.rstrip('\x00').strip().upper()
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i][0]:
                i += 1
            node = node.children[i]
        # varrer esta folha _e todas as folhas à direita_ 
        results = []
        while node:
            for k, offsets in node.keys:
                # garanta mesmo formato antes de comparar
                if k.rstrip('\x00').strip().upper() == key:
                    results.extend(offsets)
                elif k > key:
                    # já passou da chave
                    return results
            node = node.next
        return results

    def save(self):
        """
        Serializa a árvore B+ em disco usando pickle.
        """
        if self.index_file:
            with open(self.index_file, 'wb') as f:
                pickle.dump(self, f)

    def load(self):
        """
        Carrega a árvore B+ do disco.
        """
        with open(self.index_file, 'rb') as f:
            tree = pickle.load(f)
            self.root = tree.root
            self.order = tree.order

    def keys(self):
        """
        Retorna todas as chaves indexadas, ordenadas.
        """
        result = []
        node = self.root
        # Vai até a folha mais à esquerda
        while not node.leaf:
            node = node.children[0]
        # Percorre todas as folhas
        while node:
            result.extend([k for k, _ in node.keys])
            if hasattr(node, 'next'):
                node = node.next
            else:
                break
        return result