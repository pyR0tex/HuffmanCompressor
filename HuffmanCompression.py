# HuffmanCompression.py
from collections import Counter
import heapq

class HuffmanNode:
    def __init__(self, char=None, frequency=None):
        self.left = None
        self.right = None
        self.char = char
        self.frequency = frequency

    def __str__(self):
        return (f"Node: (char - {self.char}) (frequency - {self.frequency})")

    def __lt__(self, other):
        return self.frequency < other.frequency
    
def getFrequency(fileContent):
    '''
    Returns a dictionary with each characters' frequency
    '''
    content = fileContent

    frequency_unsorted = Counter(content)
    frequency_sorted = sorted(frequency_unsorted.items(), key=lambda item: item[1])
    frequency = dict(frequency_sorted[::-1])
    # print(f"      Frequencies: \n {dict(frequency)}")
    return frequency

def buildHuffmanTree(nodes: dict) -> HuffmanNode:
    priorityQueue = [HuffmanNode(char=char, frequency=f) for char, f in (nodes.items())]
    heapq.heapify(priorityQueue)

    while len(priorityQueue) > 1:
        left = heapq.heappop(priorityQueue)
        right = heapq.heappop(priorityQueue)
        internalNode = HuffmanNode(frequency= left.frequency+right.frequency)
        internalNode.left = left
        internalNode.right = right
        heapq.heappush(priorityQueue, internalNode)
    return priorityQueue[0]

def generateHuffmanCodes(node: HuffmanNode, binaryCode="", huffmanCodes={}) -> dict:
    if node is not None:
        if node.char is not None:
            huffmanCodes[node.char] = binaryCode
        generateHuffmanCodes(node.left, binaryCode+"0", huffmanCodes)
        generateHuffmanCodes(node.right, binaryCode+"1", huffmanCodes)
    return huffmanCodes
    
def generateBinaryCode(binaryCodes, fileContent):
    code = ""
    for char in fileContent:
        code += binaryCodes[char]
    return code

# return the huffman codes
def encode(content: str) -> dict:
    encoded = {}
    frequency = getFrequency(content)
    huffmanTree = buildHuffmanTree(frequency)
    binaryCodes = generateHuffmanCodes(huffmanTree)
    binaryCode = generateBinaryCode(binaryCodes, content)
    encoded["frequency"] = frequency
    encoded["codes"] = binaryCodes
    encoded["binaryCode"] = binaryCode

    return encoded

def decode(frequency: dict, binaryCode: str) -> str:
    decoded = ""
    root = buildHuffmanTree(frequency)
    curr = root
    for char in binaryCode:
        if curr.char is not None:
            decoded += curr.char
            curr = root
        if char == '0':
            curr = curr.left
        elif char == '1':
            curr = curr.right
    decoded += curr.char
    # print(decoded)
    return decoded