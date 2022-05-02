class Node:
    def __init__(self, _tuple, left=None, right=None):
        self.symbol = _tuple[0]
        self.freq = _tuple[1]
        self.left = left
        self.right = right
        self.value = ''


class Huffman:
    encoded_dict = {}
    decoded_data = []
    sign_freq = {}
    data = ''

    def __init__(self, data, tree_root = None):
        self.data = data
        self.tree_root = tree_root

    def calc_freq(self, data):
        for i in data:
            if i in self.sign_freq.keys():
                self.sign_freq[i] += 1
            else:
                self.sign_freq[i] = 1

    def create_tree(self):
        nodes = [Node(el) for el in list(self.sign_freq.items())]
        nodes = sorted(nodes, key=lambda x: x.freq)

        while len(nodes) > 1:
            left = nodes[0]
            right = nodes[1]

            left.value = 0
            right.value = 1
            parentNode = Node((left.symbol + right.symbol, left.freq + right.freq), left, right)

            nodes.remove(left)
            nodes.remove(right)
            nodes.append(parentNode)

        self.tree_root = nodes[0]

    def create_encoded_dict(self, node, val=''):
        new_val = val + str(node.value)
        if node.left:
            self.create_encoded_dict(node.left, new_val)
        if node.right:
            self.create_encoded_dict(node.right, new_val)
        if node.left is None and node.right is None:
            self.encoded_dict[node.symbol] = new_val

    def encode(self):
        self.calc_freq(self.data)
        self.create_tree()
        self.create_encoded_dict(self.tree_root)
        encoded_data = ''
        for i in self.data:
            encoded_data += self.encoded_dict[i]
        return encoded_data

    def search(self, node, i):
        if node.left is None and node.right is None:
            self.decoded_data.append(node.symbol)
            if i + 1 < len(self.data):
                self.search(self.tree_root, i)
        else:
            if self.data[i + 1] == '0':
                self.search(node.left, i + 1)
            else:
                self.search(node.right, i + 1)

    def decode(self):
        self.search(self.tree_root, -1)
        result = ''
        for sign in self.decoded_data:
            result += sign
        return result