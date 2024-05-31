#!/usr/bin/env python3
import hashlib
import json
import logging
from time import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_logs = []
        self.new_block(previous_hash='1', proof=100)  # Genesis block

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'logs': self.current_logs,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_logs = []
        self.chain.append(block)
        logging.info(f'New block added: {block}')
        return block

    def new_log(self, user, log_entry):
        log = {
            'user': user,
            'log_entry': log_entry,
            'timestamp': time(),
        }
        self.current_logs.append(log)
        logging.info(f'New log entry added: {log}')
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        logging.info(f'Proof of work found: {proof}')
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block['previous_hash'] != self.hash(previous_block):
                logging.error(f'Invalid block hash at index {i}')
                return False
            if not self.valid_proof(previous_block['proof'], current_block['proof']):
                logging.error(f'Invalid proof of work at index {i}')
                return False
        logging.info('Blockchain is valid.')
        return True

if __name__ == '__main__':
    blockchain = Blockchain()

    blockchain.new_log(user="Alice", log_entry="User Alice logged in.")
    blockchain.new_log(user="Bob", log_entry="User Bob accessed confidential data.")


    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)


    previous_hash = blockchain.hash(blockchain.last_block)
    blockchain.new_block(proof, previous_hash)
    
  
    print(json.dumps(blockchain.chain, indent=4))

  
    is_valid = blockchain.validate_chain()
    print(f'Blockchain valid: {is_valid}')
