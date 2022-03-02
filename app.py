import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

#Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

#Cache the contract on load
@st.cache(allow_output_mutation=True)

# Define the load_contract function
def load_contract():
    
    with open(Path('certificate_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract

#load contract
contract=load_contract()


st.title("March Madness Tournament!")
st.write("So you think you can pick the winner of this year's tourney? :sunglasses:")
st.write("You can bid on each team that you think will win. Buyer of the winning team will win the entire pool.")

teams = contract.functions.show
st.write("The current teams in contention are:")

#round1winners = st.multiselect(
    #"")
    
teamId=1
auction_result = contract.functions.auctionResult(0).call()
contract_owner = contract.functions.contractOwner.call()
#st.write(f"{auction_result}")
#st.write(f"{contract_owner}")

#auction_end_time = auction_result[0]
#st.write(f"Auction End Time {auction_end_time}")

#st.code(contract.abi[7]["outputs"][0])
st.write("Current Highest Bidder")
st.code(contract.abi[7]["outputs"][1])
st.write("Current Highest Bid")
st.code(contract.abi[7]["outputs"][2])
        #["outputs"]["highestBidder"])


_teamId = st.text_input("Which team are you bidding for?")
bidvalue = st.text_input("Bid Amount?")
if st.button("bid"):  
    #contract.functions.bid(int(_teamId))
    contract.functions.bid(int(_teamId)).transact({"value": bidvalue})
    
    
#how to incorporate the value amount?


