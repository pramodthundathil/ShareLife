# Block chain Calculations-----------------------------------------------------


import hashlib
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
    def __str__(self):
        return "Block index: " + str(self.index) + "\n" + \
               "Block timestamp: " + str(self.timestamp) + "\n" + \
               "Block data: " + str(self.data) + "\n" + \
               "Block previous_hash: " + str(self.previous_hash) + "\n" + \
               "Block hash: " + str(self.hash)
    
def create_genesis_block():
    # Manually create the first block with arbitrary data
    return Block(0, datetime.now(), {'name': 'John Doe', 'email': 'johndoe@example.com', 'password': 'mypassword'}, "0")

blockchain = [create_genesis_block()]


def add_block(data):
    previous_block = blockchain[-1]
    index = previous_block.index + 1
    timestamp = datetime.now()
    previous_hash = previous_block.hash
    new_block = Block(index, timestamp, data, previous_hash)
    blockchain.append(new_block)
    
    
def is_valid_chain(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]
        if current_block.hash != current_block.calculate_hash():
            return False
        if current_block.previous_hash != previous_block.hash:
            return False
    return True