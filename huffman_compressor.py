"""
Implementation of archivator using Huffman coding
works only with alphanumeric symbols, ASCII 0-255
"""

from collections import Counter
from queue import PriorityQueue
import os


class HuffmanNode:
    def __init__(self, char, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def encode(text):
    """Returns encoded string code with format [encoded_huffman_tree][extra_zeros_num][encoded_text]"""

    frequencies = Counter(text)
    queue = PriorityQueue()
    code_table = {}

    for char, f in frequencies.items():
        queue.put(HuffmanNode(char, f))

    # merge nodes
    while queue.qsize() > 1:
        l, r = queue.get(), queue.get()
        queue.put(HuffmanNode(None, l.freq + r.freq, l, r))

    huffman_tree = queue.get()

    _fill_code_table(huffman_tree, "", code_table)

    encoded_text_code = ""
    for c in text:
        encoded_text_code += code_table[c]

    encoded_tree_code = _encode_huffman_tree(huffman_tree, "")

    # add extra zeros, as in python it is not possible read
    # file bit by bit (min byte) so extra zeros will be
    # added automatically which cause a loss of information
    num = 8 - (len(encoded_text_code) + len(encoded_tree_code)) % 8
    if num != 0:
        encoded_text_code = num * "0" + encoded_text_code

    print(f"frequencies: {frequencies}")
    print(f"encoded huffman tree code: {encoded_tree_code}")
    print(f"encoded text code: {encoded_text_code}")

    return f"{encoded_tree_code}{num:08b}{encoded_text_code}"


def decode(encoded_text):
    """Returns decoded string"""

    encoded_text_ar = list(encoded_text)
    encoded_tree = _decode_huffman_tree(encoded_text_ar)

    # remove extra zeros
    number_of_extra_0_bin = encoded_text_ar[:8]
    encoded_text_ar = encoded_text_ar[8:]
    number_of_extra_0 = int("".join(number_of_extra_0_bin), 2)
    encoded_text_ar = encoded_text_ar[number_of_extra_0:]

    # decode text
    text = ""
    current_node = encoded_tree
    for char in encoded_text_ar:
        current_node = current_node.left if char == '0' else current_node.right

        if current_node.char is not None:
            text += current_node.char
            current_node = encoded_tree

    return text


def decompress(input_path, output_path):
    """Save decoded text to output file"""

    with open(input_path, "rb") as in_file, open(output_path, "w") as out_file:
        encoded_text = ""

        byte = in_file.read(1)
        while len(byte) > 0:
            encoded_text += f"{bin(ord(byte))[2:]:0>8}"
            byte = in_file.read(1)

        decoded_text = decode(encoded_text)
        out_file.write(decoded_text)


def compress(input_path, output_path):
    """Save encoded text to output file"""

    with open(input_path) as in_file, open(output_path, "wb") as out_file:
        text = in_file.read()
        encoded_text = encode(text)

        b_arr = bytearray()
        for i in range(0, len(encoded_text), 8):
            b_arr.append(int(encoded_text[i:i+8], 2))

        out_file.write(b_arr)


def _fill_code_table(node, code, code_table):
    """Fill code table, which has chars and corresponded codes"""

    if node.char is not None:
        code_table[node.char] = code
    else:
        _fill_code_table(node.left, code + "0", code_table)
        _fill_code_table(node.right, code + "1", code_table)


def _encode_huffman_tree(node, tree_text):
    """Encode huffman tree to save it in the file"""

    if node.char is not None:
        tree_text += "1"
        tree_text += f"{ord(node.char):08b}"
    else:
        tree_text += "0"
        tree_text = _encode_huffman_tree(node.left, tree_text)
        tree_text = _encode_huffman_tree(node.right, tree_text)

    return tree_text


def _decode_huffman_tree(tree_code_ar):
    """Decoding huffman tree to be able to decode the encoded text"""

    # need to delete each use bit as we don't know the length of it and
    # can't separate it from the text code
    code_bit = tree_code_ar[0]
    del tree_code_ar[0]

    if code_bit == "1":
        char = ""
        for _ in range(8):
            char += tree_code_ar[0]
            del tree_code_ar[0]

        return HuffmanNode(chr(int(char, 2)))

    return HuffmanNode(None, left=_decode_huffman_tree(tree_code_ar), right=_decode_huffman_tree(tree_code_ar))


def _print_ratio(input_path, output_path):
    before_size = os.path.getsize(input_path)
    after_size = os.path.getsize(output_path)
    compression_percent = round(100 - after_size / before_size * 100, 1)
    print(f"before: {before_size}bytes, after: {after_size}bytes, "
          f"compression {compression_percent}%")



'''file_to_compress, decompressed, compressed = "image.txt", "decompressed.txt", "compressed.bin"
compress(file_to_compress, compressed)'''
    


