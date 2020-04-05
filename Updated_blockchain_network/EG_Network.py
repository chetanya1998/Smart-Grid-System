# Blockchain for Smart Grid System
# importing libraries
import datetime
import hashlib
import json
from flask import Flask ,jsonify
#blockchain devpart
class SG_network:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
#Mechanism for creating new block for transaction record
    def create_block(self,proof,previous_hash):
        block = {'index':len(self.chain) + 1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash,
                 }
        self.chain.append(block)
        return block
#function to return previous block of transaction
    def get_previous_block(self):
        return self.chain[-1]
#POW Algorithm - to avoid 51% majority attack
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
#Block verification system based on POW(proof_of_work)
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index <len(chain):
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
#Mining Process
        #A Web App
        

app = Flask(__name__)
        
#creating a blockchain for Smart Grid

sg = SG_network()

#Mining a blockchain

#route for adding new block of transaction in Smart Grid SG_network
@app.route('/mine_block',methods = ['GET'])
def mine_block():
    previous_block = sg.get_previous_block()
    previous_proof = previous_block['proof']
    proof = sg.proof_of_work(previous_proof)
    previous_hash = sg.hash(previous_block)
    block = sg.create_block(proof, previous_hash)
    response = {'message:':'Congratulations,you just added a new block of transaction',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']
                }
    return jsonify(response),200
# route for viewing or getting information of all transactions in Smart_Grid network
@app.route('/get_chain',methods = ['GET'])
def get_chain():
    response = {'chain':sg.chain,
                'length':len(sg.chain)}
    return jsonify(response), 200

# run app


app.run(host='0.0.0.0',port = 5000)
            
            
    
