#Blockchain System for Decentralised Smart Grid Technology
**Blockchain.py - faulty test version**

**Blockchain2.py - is correct version with the implementation of sha256 hashing algorithm**

**Blockchain3.py - is undertest version with the implementation of sha512 hashing algorithm**

#Under Development Backend Based Blockachain Application for Smart Grid Technology
##How to execute flask based web application of blockchain implemented in python

**Step1-Install Postman on your PC**

**Step2-Download blockchain.py file & install flask package of version 0.12.2(using below command) on your PC**
pip install Flask==0.12.2

**Step3-run blockchain.py file in Anaconda Spyder IDE(preferable)**

**Step4-Open Postman web/desktop application and choose GET method**

**Step5-Type the following request in GET Request of Postman application**
http://127.0.0.1:5000/get_chain - it will show blockchain starting from genesis block

**Step6-Type the following request in GET Request of Postman application for mining more blocks in blockchain**
http://127.0.0.1:5000/mine_block - it will mine more blocks into a blockchain (in simple terms adding more blocks in to chain and form blockchain)



