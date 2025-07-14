import requests
import json
import time

def test_blockchain_network():
    """
    Test the blockchain P2P network functionality
    """
    # Node URLs
    node1_url = 'http://localhost:5001'
    node2_url = 'http://localhost:5002'
    node3_url = 'http://localhost:5003'
    
    print("=== Testing Blockchain P2P Network ===")
    
    # Test 1: Check if nodes are running
    print("\n1. Testing node connectivity...")
    try:
        response1 = requests.get(f'{node1_url}/')
        response2 = requests.get(f'{node2_url}/')
        response3 = requests.get(f'{node3_url}/')
        print("✓ All nodes are running")
    except Exception as e:
        print(f"✗ Error connecting to nodes: {e}")
        return
    
    # Test 2: Register nodes with each other
    print("\n2. Registering nodes...")
    nodes_to_register = [node2_url, node3_url]
    
    # Register nodes on node1
    response = requests.post(f'{node1_url}/nodes/register', 
                           json={'nodes': nodes_to_register})
    print(f"Node 1 registration: {response.json()}")
    
    # Register nodes on node2
    nodes_to_register = [node1_url, node3_url]
    response = requests.post(f'{node2_url}/nodes/register', 
                           json={'nodes': nodes_to_register})
    print(f"Node 2 registration: {response.json()}")
    
    # Register nodes on node3
    nodes_to_register = [node1_url, node2_url]
    response = requests.post(f'{node3_url}/nodes/register', 
                           json={'nodes': nodes_to_register})
    print(f"Node 3 registration: {response.json()}")
    
    # Test 3: Add transactions
    print("\n3. Adding transactions...")
    transactions = [
        {'from': 'Alice', 'to': 'Bob', 'amount': 50},
        {'from': 'Bob', 'to': 'Charlie', 'amount': 25},
        {'from': 'Charlie', 'to': 'Alice', 'amount': 10}
    ]
    
    for tx in transactions:
        response = requests.post(f'{node1_url}/transactions/new', json=tx)
        print(f"Added transaction: {tx}")
    
    # Test 4: Mine a block
    print("\n4. Mining block on Node 1...")
    response = requests.post(f'{node1_url}/mine')
    print(f"Mining result: {response.json()['message']}")
    
    # Test 5: Check chain lengths
    print("\n5. Checking chain lengths...")
    chain1 = requests.get(f'{node1_url}/chain').json()
    chain2 = requests.get(f'{node2_url}/chain').json()
    chain3 = requests.get(f'{node3_url}/chain').json()
    
    print(f"Node 1 chain length: {chain1['length']}")
    print(f"Node 2 chain length: {chain2['length']}")
    print(f"Node 3 chain length: {chain3['length']}")
    
    # Test 6: Sync chains (consensus)
    print("\n6. Running consensus algorithm...")
    response2 = requests.get(f'{node2_url}/nodes/resolve')
    response3 = requests.get(f'{node3_url}/nodes/resolve')
    
    print(f"Node 2 consensus: {response2.json()['message']}")
    print(f"Node 3 consensus: {response3.json()['message']}")
    
    # Test 7: Verify synchronization
    print("\n7. Verifying synchronization...")
    chain1 = requests.get(f'{node1_url}/chain').json()
    chain2 = requests.get(f'{node2_url}/chain').json()
    chain3 = requests.get(f'{node3_url}/chain').json()
    
    print(f"Node 1 chain length: {chain1['length']}")
    print(f"Node 2 chain length: {chain2['length']}")
    print(f"Node 3 chain length: {chain3['length']}")
    
    # Test 8: Check balances
    print("\n8. Checking balances...")
    addresses = ['Alice', 'Bob', 'Charlie', 'node_5001']
    
    for address in addresses:
        balance = requests.get(f'{node1_url}/balance/{address}').json()
        print(f"{address}: {balance['balance']}")
    
    # Test 9: Validate blockchain
    print("\n9. Validating blockchain...")
    validation = requests.get(f'{node1_url}/validate').json()
    print(f"Blockchain validation: {validation['message']}")
    
    print("\n=== Test Complete ===")

if __name__ == '__main__':
    test_blockchain_network()
