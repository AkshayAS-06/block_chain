import hashlib
import json
import time
from urllib.parse import urlparse
import requests

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        """
        Initialize a new block in the blockchain
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate the hash of the block using SHA-256
        """
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """
        Mine the block using Proof of Work algorithm
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")
        return self.hash

class Blockchain:
    def __init__(self):
        """
        Initialize the blockchain with genesis block
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 10
        self.nodes = set()
    
    def create_genesis_block(self):
        """
        Create the first block in the blockchain
        """
        return Block(0, [], time.time(), "0")
    
    def get_latest_block(self):
        """
        Get the most recent block in the chain
        """
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        """
        Add a new transaction to the pending transactions
        """
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self, mining_reward_address):
        """
        Mine all pending transactions and add them to the blockchain
        """
        # Add mining reward transaction
        reward_transaction = {
            'from': None,
            'to': mining_reward_address,
            'amount': self.mining_reward
        }
        self.pending_transactions.append(reward_transaction)
        
        # Create new block with pending transactions
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )
        
        # Mine the block
        block.mine_block(self.difficulty)
        
        # Add block to chain and reset pending transactions
        self.chain.append(block)
        self.pending_transactions = []
    
    def get_balance(self, address):
        """
        Calculate the balance for a given address
        """
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('from') == address:
                    balance -= transaction.get('amount', 0)
                if transaction.get('to') == address:
                    balance += transaction.get('amount', 0)
        
        return balance
    
    def is_chain_valid(self):
        """
        Validate the entire blockchain
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def register_node(self, address):
        """
        Register a new node in the network
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def resolve_conflicts(self):
        """
        Consensus algorithm: replace chain with longest valid chain
        """
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        
        # Check all nodes in network
        for node in neighbours:
            try:
                response = requests.get(f'http://{node}/chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
                    
                    # Check if chain is longer and valid
                    if length > max_length and self.is_valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except:
                continue
        
        # Replace chain if longer valid chain found
        if new_chain:
            self.chain = [self.dict_to_block(block_data) for block_data in new_chain]
            return True
        
        return False
    
    def is_valid_chain(self, chain):
        """
        Validate a blockchain received from another node
        """
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]
            
            # Reconstruct hash to verify
            block_string = f"{current_block['index']}{current_block['transactions']}{current_block['timestamp']}{current_block['previous_hash']}{current_block['nonce']}"
            calculated_hash = hashlib.sha256(block_string.encode()).hexdigest()
            
            if current_block['hash'] != calculated_hash:
                return False
            
            if current_block['previous_hash'] != previous_block['hash']:
                return False
        
        return True
    
    def dict_to_block(self, block_data):
        """
        Convert dictionary to Block object
        """
        block = Block(
            block_data['index'],
            block_data['transactions'],
            block_data['timestamp'],
            block_data['previous_hash'],
            block_data['nonce']
        )
        block.hash = block_data['hash']
        return block
    
    def block_to_dict(self, block):
        """
        Convert Block object to dictionary for JSON serialization
        """
        return {
            'index': block.index,
            'transactions': block.transactions,
            'timestamp': block.timestamp,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash': block.hash
        }
    
    def get_chain_as_dict(self):
        """
        Get the entire blockchain as a list of dictionaries
        """
        return [self.block_to_dict(block) for block in self.chain]
