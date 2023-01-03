import hashlib
import pandas as pd
import streamlit as st
from typing import List  
from typing import Any, List
from datetime import datetime
from dataclasses import dataclass
#
st.set_page_config(layout="wide")
st.title("# Blockchain illustration with multiple transactions") 
st.write("By Y.X. Yan, v1.0, 1/10/2023")
a1=f"##### A blockchain is a distributed database or ledger that is shared among "
a2="the nodes of a computer network. For this illustration, you can enter your"
a3=" transactions, see how the ledge building up, inspect each transaction, "
a4=" and save your data to a csv file called blockchain.csv. Please pay attention"
a5=" to two things: 1) each transaction has its unique hash (64-character long) by using the"
a6=" hashlib.sha256() function, and 2) it has its previous hash attached (except for the first one)."
a7=" To see column 2 completely, refresh your screen after entering your first transaction."
#
with st.expander(" Click here to see and hide the explanation:"):
    st.write(a1+a2+a3+a4+a5+a6+a7)
#st.write(" .   ")
#st.write(" .   ")
#st.write(" .   ")
#st.write(" .   ")
#st.write(".")
col1, col2,col3 =st.columns([0.5,2.0,1.5])
@dataclass   
class RecordTrade:
    buyer_id: str
    seller_id: str
    shares: float
@dataclass            # Block class
class Block:
    record: RecordTrade
    trade_time: str = datetime.utcnow().strftime("%Y:%m:%d:%H:%M:%S")
    prev_hash: str = "0"
    def hash_block(self):
        sha = hashlib.sha256()                         # using the function 
        trade_time_encoded = self.trade_time.encode()  # Encode the time of trade
        sha.update(trade_time_encoded)                 # Add the encoded trade time into the hash
        record = str(self.record).encode()             # Encode the Record class
        sha.update(record)                             # Then hash it
        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)
        return sha.hexdigest() # Return the hash to the rest of the Block class
@dataclass                     # StockChain class
class StockChain:
    chain: List[Block]         # The class `StockChain` holds a list of blocks
    def add_block(self, block):# The function `add_block` adds any new `block` to the `chain` list
        self.chain += [block]
#
col1.write("## Part 1: Enter transactions") 
buyer = col1.text_input("Enter a buyer's ID below:") 
seller = col1.text_input("Enter a seller's ID below:")
shares = col1.text_input("Enter the amount below:")
#
@st.cache(allow_output_mutation=True)         # Set up the web app for deployment
def setup():
    genesis_block = Block(record=RecordTrade(shares=100, buyer_id=1, seller_id=2))
    #genesis_block = Block(record=RecordTrade(shares, buyer_id, seller_id))
    return StockChain([genesis_block])
stockchain_live = setup()                     # Serve the web app
#
if st.button("Click here to add"):            # add a button
    prev_block = stockchain_live.chain[-1]    # Pull the original block to start on
    prev_block_hash = prev_block.hash_block() # Hash the original block (to put into the next block)
    new_block = Block(record=RecordTrade(buyer, seller, shares),prev_hash=prev_block_hash)
    stockchain_live.add_block(new_block)      # Add the new_block to the existing chain
    st.balloons()                             # Just for fun, we add a little pizzazz
#
col2.write("## Blockchain ledger (refresh after the 1st transaction)") 
stockchain_df = pd.DataFrame(stockchain_live.chain).astype(str) # Save the data from the blockchain as a DataFrame
col2.write(stockchain_df)                       # display the DataFrame data
# ------- part 3----------------------
col3.write("## Part 2: Inspect individual blocks")    # dropdown menu to select which block in the chain to display
selected_block =col3.selectbox("Which block would you like to inspect?", stockchain_live.chain)
col3.write(selected_block)                           # Display the selected block on the sidebar
col3.write("## Part 3: Download to blockchain.csv")  # dropdown menu to select which block in the chain to display
stockchain_df.index.name ="N"
csv = stockchain_df.to_csv().encode('utf-8')         # download 
a=col3.download_button("Click here to download",csv,"blockchain.csv","text/csv",key='download-csv')
if a==True:
    col3.balloons()      
# ----- part 5 ---------------
#col3.write("# Part 5: clear")        
#if col3.button("Click here to clear"):
    #col3.write('place holder')
    #del stockchain_df
    #stockchain_live = setup()     
 #   caching.clear_cache()
    #click on the ☰ menu, then “Clear cache”. 
with st.expander(" Click here to learn how to clear cache."):
    st.write("#### Click on the triple bar (☰) menu (at the top-right corner), 'Clear cache', then refresh your screen.")