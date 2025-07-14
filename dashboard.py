from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

# Configuration
NODES = [
    'http://localhost:5001',
    'http://localhost:5002', 
    'http://localhost:5003'
]

@app.route('/')
def dashboard():
    """
    Main dashboard showing all nodes
    """
    node_data = []
    for node_url in NODES:
        try:
            response = requests.get(f'{node_url}/chain')
            if response.status_code == 200:
                data = response.json()
                node_data.append({
                    'url': node_url,
                    'chain_length': data['length'],
                    'status': 'online'
                })
            else:
                node_data.append({
                    'url': node_url,
                    'chain_length': 0,
                    'status': 'error'
                })
        except:
            node_data.append({
                'url': node_url,
                'chain_length': 0,
                'status': 'offline'
            })
    
    return render_template('dashboard.html', nodes=node_data)

@app.route('/node/<path:node_url>')
def node_detail(node_url):
    """
    Show detailed information about a specific node
    """
    try:
        response = requests.get(f'{node_url}/chain')
        chain_data = response.json()
        
        nodes_response = requests.get(f'{node_url}/nodes')
        nodes_data = nodes_response.json()
        
        return render_template('node_detail.html', 
                             node_url=node_url,
                             chain=chain_data,
                             registered_nodes=nodes_data)
    except Exception as e:
        return f"Error connecting to node: {e}"

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """
    Add a new transaction
    """
    from_addr = request.form['from']
    to_addr = request.form['to']
    amount = float(request.form['amount'])
    node_url = request.form['node_url']
    
    transaction = {
        'from': from_addr,
        'to': to_addr,
        'amount': amount
    }
    
    try:
        response = requests.post(f'{node_url}/transactions/new', json=transaction)
        if response.status_code == 201:
            return redirect(url_for('dashboard'))
        else:
            return f"Error adding transaction: {response.text}"
    except Exception as e:
        return f"Error connecting to node: {e}"

@app.route('/mine/<path:node_url>')
def mine_block(node_url):
    """
    Mine a new block on the specified node
    """
    try:
        response = requests.post(f'{node_url}/mine')
        if response.status_code == 200:
            return redirect(url_for('dashboard'))
        else:
            return f"Error mining block: {response.text}"
    except Exception as e:
        return f"Error connecting to node: {e}"

@app.route('/sync/<path:node_url>')
def sync_node(node_url):
    """
    Sync the specified node with the network
    """
    try:
        response = requests.get(f'{node_url}/nodes/resolve')
        if response.status_code == 200:
            return redirect(url_for('dashboard'))
        else:
            return f"Error syncing node: {response.text}"
    except Exception as e:
        return f"Error connecting to node: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=8080)
