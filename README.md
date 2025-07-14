# block_chain
Blockchain P2P Network Simulation

A simple, educational peer-to-peer blockchain network written in Python using Flask. Each node runs independently, maintains its own blockchain, and syncs with peers using a basic consensus algorithm.
Features
Simple blockchain with transaction and block structures
Proof-of-Work mining (adjustable difficulty)
Multiple Flask nodes on different ports (P2P simulation)
Node discovery and registration
Longest chain consensus algorithm
Manual blockchain synchronization between peers
(Bonus) Web dashboard for monitoring and interacting with the network
File Structure
text
blockchain-p2p/
│
├── blockchain.py          # Blockchain and Block class definitions
├── node.py                # Flask app for running a blockchain node
├── test_network.py        # Script to test multi-node network and consensus
├── dashboard.py           # (Bonus) Flask dashboard for visualizing nodes
│
├── requirements.txt       # List of required packages (Flask, requests)
├── README.md              # This file
│
├── start_nodes.bat        # (Windows) Batch script to start multiple nodes
├── start_nodes.sh         # (Linux/Mac) Shell script to start multiple nodes
│
└── templates/             # (Bonus) HTML templates for the dashboard
    ├── dashboard.html
    └── node_detail.html
Requirements
Python 3.7+
Flask
requests
Install dependencies with:
bash
pip install -r requirements.txt
How to Run
1. Start the Blockchain Nodes
Open separate terminals and run:
bash
python node.py -p 5000
python node.py -p 5001
python node.py -p 5002
Or use the provided script:
Windows: start_nodes.bat
Mac/Linux: ./start_nodes.sh
2. Test the Network
Run the test script to simulate transactions, mining, and consensus:
bash
python test_network.py
3. (Optional) Start the Dashboard
Run the dashboard server:
bash
python dashboard.py
Then open your browser and visit: http://localhost:8080/
API Endpoints
Each node exposes the following REST API endpoints:
Endpoint	Method	Description
/	GET	Node status message
/chain	GET	Returns the full blockchain
/mine	POST	Mines a new block with pending transactions
/transactions/new	POST	Adds a new transaction
/balance/<address>	GET	Returns balance for an address
/nodes/register	POST	Registers new peer nodes
/nodes/resolve	GET	Runs consensus to sync with peers
/nodes	GET	Lists all registered peer nodes
/validate	GET	Validates the blockchain
Usage Workflow
Register nodes: Each node learns about its peers using /nodes/register.
Add transactions: Use /transactions/new to submit new transactions.
Mine blocks: Use /mine to include pending transactions in a new block.
Sync chains: Use /nodes/resolve (or the dashboard "Sync" button) to synchronize nodes using the longest valid chain.
Check balances: Query /balance/<address> to see account balances.
Monitor network: Use the dashboard for a visual overview and interaction.
Dashboard Features (Bonus)
View all node statuses and chain lengths
Add transactions through a web form
Mine new blocks from the dashboard
Sync nodes with the network
View detailed chain and peer info for each node
Example requirements.txt
text
Flask
requests
Project Architecture
Block: Contains index, transactions, timestamp, previous hash, nonce, and hash
Blockchain: Manages the chain, mining, transaction pool, and consensus
Node: Flask server exposing REST API for blockchain operations
Consensus: Implements the "longest chain wins" rule for synchronization
Dashboard: (Bonus) Flask app with HTML templates for network monitoring
Notes
The blockchain is for educational/demo purposes and is not secure for real-world use.
Transactions are only included in the blockchain after mining a new block.
Nodes must be manually synced for their chains to update after another node mines a block.
The dashboard and templates are optional but recommended for easier interaction.
