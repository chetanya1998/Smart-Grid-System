#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 04:23:20 2020

@author: chetanya
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import hashlib
import json
from flask import Flask ,jsonify, request
import requests
from uuid import uuid4 
from urllib.parse import urlparse
# Smart Grid_ network development part
class SG_network:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
    def create_block(self,proof,previous_hash):
        block = {'index':len(self.chain) + 1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash,
                 'transaction':self.transactions
                 }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain [block_index]
            if block['previous_hash'] !=self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block = block
            block_index += 1
        return True
    # add_transaction function keeps the track of transactions in a chain
    def add_transaction(self, sender_address, reciever_address, units,Ether):
        self.transactions.append({'sender_address':sender_address,
                                  'reciever_address':reciever_address,
                                  'units':units,
                                  'Ether':Ether
                                  })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    # decentralization gets started from this function
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
               length = response.json()['length']
               chain = response.json()['chain']
               if length > max_length and self.is_chain_valid(chain):
                   max_length = length
                   longest_chain =chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
        
                   
            
#Mining Process
#A Web App
        
app = Flask(__name__)

#creating an address for the node on port 5000
node_address = str(uuid4()).replace('-','')
        
#creating Smart_Grid sg

sg = SG_network()

#Adding New Block of transaction
@app.route('/mine_block',methods = ['GET'])
def mine_block():
    previous_block = sg.get_previous_block()
    previous_proof = previous_block['proof']
    proof = sg.proof_of_work(previous_proof)
    previous_hash = sg.hash(previous_block)
    sg.add_transaction(sender_address = node_address, reciever_address = '52-B', units = 10,Ether=5 )
    block = sg.create_block(proof, previous_hash)
    response = {'message:':'Congratulations,your power transaction is successful',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash'],
                'transactions':block['transaction']}
    return jsonify(response),200
#route will show complete details of complete chain transactions
@app.route('/get_chain',methods = ['GET'])
def get_chain():
    response = {'chain':sg.chain,
                'length':len(sg.chain)}
    return jsonify(response), 200
#verifying power transaction block for supply is valid or not 
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = sg.is_chain_valid(sg.chain)
    if is_valid:
        response = {'message': 'All good!. The block of transaction is valid.'}
    else:
        response = {'message': 'Sir, we have a problem. The block of transaction is not valid.'}
    return jsonify(response), 200

# Adding a  new transaction to the Smart Grid Network
@app.route('/add_transaction',methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender_address','reciever_address','units','Ether']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing',400
    index = sg.add_transaction(json['sender_address'],json['reciever_address'],json['units'],json['Ether'])
    response = {'message':f'This transaction will be added to Block{index}'}
    return jsonify(response), 201
#sg Decentralising 
    
#Connecting new nodes
@app.route('/connect_node',methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node",400
    for node in nodes:
        sg.add_node(node)
    response ={'message':'All the Addresses are now connected.The Smart_Grid network now contains following Address`s',
            'total_nodes':list(sg.nodes)}
    return jsonify(response),201

#replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced= sg.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The address had different chains so the chain was replaced by the longest one',
                    'new_chain':sg.chain}
    else:
        response = {'message': 'All good. the chain is the original one.',
                    'actual_chain':sg.chain}
    return jsonify(response), 200
    
#run app
app.run(host='0.0.0.0',port = 5002)
            
