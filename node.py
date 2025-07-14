from flask import Flask, jsonify, request
import argparse
import json
from blockchain import Blockchain
import threading
import time

class BlockchainNode:
    def __init__(self, port):
        self.app = Flask(__name__)
        self.blockchain = Blockchain()
        self.port = port
        self.node_id = f"node_{port}"
        self.setup_routes()
    
    def setup_routes(self):
        """
        Set up all Flask routes for the node
        """
        
        @self.app.route('/')
        def index():
            return f"Blockchain Node running on port {self.port}"
        
        @self.app.route('/chain', methods=['GET'])
        def get_chain():
            """
            Get the full blockchain
            """
            response = {
                'chain': self.blockchain.get_chain_as_dict(),
                'length': len(self.blockchain.chain)
            }
            return jsonify(response), 200
        
        @self.app.route('/mine', methods=['POST'])
        def mine():
            """
            Mine a new block
            """
            self.blockchain.mine_pending_transactions(self.node_id)
            
            latest_block = self.blockchain.get_latest_block()
            response = {
                'message': 'New block mined successfully',
                'block': self.blockchain.block_to_dict(latest_block)
            }
            return jsonify(response), 200
        
        @self.app.route('/transactions/new', methods=['POST'])
        def new_transaction():
            """
            Add a new transaction
            """
            values = request.get_json()
            
            # Check required fields
            required = ['from', 'to', 'amount']
            if not all(k in values for k in required):
                return 'Missing values', 400
            
            # Add transaction to pending transactions
            self.blockchain.add_transaction(values)
            
            response = {
                'message': f'Transaction will be added to next block'
            }
            return jsonify(response), 201
        
        @self.app.route('/balance/<address>', methods=['GET'])
        def get_balance(address):
            """
            Get balance for a specific address
            """
            balance = self.blockchain.get_balance(address)
            response = {
                'address': address,
                'balance': balance
            }
            return jsonify(response), 200
        
        @self.app.route('/nodes/register', methods=['POST'])
        def register_nodes():
            """
            Register new nodes in the network
            """
            values = request.get_json()
            nodes = values.get('nodes')
            
            if nodes is None:
                return "Error: Please supply a valid list of nodes", 400
            
            for node in nodes:
                self.blockchain.register_node(node)
            
            response = {
                'message': 'New nodes have been added',
                'total_nodes': list(self.blockchain.nodes)
            }
            return jsonify(response), 201
        
        @self.app.route('/nodes/resolve', methods=['GET'])
        def consensus():
            """
            Consensus algorithm - resolve conflicts
            """
            replaced = self.blockchain.resolve_conflicts()
            
            if replaced:
                response = {
                    'message': 'Our chain was replaced',
                    'new_chain': self.blockchain.get_chain_as_dict()
                }
            else:
                response = {
                    'message': 'Our chain is authoritative',
                    'chain': self.blockchain.get_chain_as_dict()
                }
            
            return jsonify(response), 200
        
        @self.app.route('/nodes', methods=['GET'])
        def get_nodes():
            """
            Get all registered nodes
            """
            response = {
                'nodes': list(self.blockchain.nodes)
            }
            return jsonify(response), 200
        
        @self.app.route('/validate', methods=['GET'])
        def validate_chain():
            """
            Validate the blockchain
            """
            is_valid = self.blockchain.is_chain_valid()
            response = {
                'valid': is_valid,
                'message': 'Blockchain is valid' if is_valid else 'Blockchain is invalid'
            }
            return jsonify(response), 200
    
    def run(self):
        """
        Run the Flask node server
        """
        self.app.run(host='0.0.0.0', port=self.port, debug=False)

if __name__ == '__main__':
    # Parse command line arguments for port
    parser = argparse.ArgumentParser(description='Blockchain Node')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port to run the node on')
    args = parser.parse_args()
    
    # Create and run the node
    node = BlockchainNode(args.port)
    print(f"Starting blockchain node on port {args.port}")
    node.run()
