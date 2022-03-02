import streamlit as st
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime 

load_dotenv('api.env')

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

now = int(datetime.now().timestamp())
team_list = contract.functions.showTeamNames().call()
st.write(f"The current teams in contention are: {team_list}")

#Dashboard Functions    
for i, team in enumerate(team_list):
    auction_result = contract.functions.auctionResult(i).call()
    auction_end_time = int(auction_result[0])
    highest_bidder = auction_result[1]
    high_bid = auction_result[2]
    st.write(f"Team Name: {team}, which is number {i}:")
    if (auction_end_time == 0):
        st.write("Auction has not started yet")
    else:
        if(now > auction_end_time):
            st.write("Auction is over!")
            st.write(f"Winning Bidder: {highest_bidder}")
        else:
            st.write(f"Auction Time Remaining(sec): {auction_end_time-now}")
            st.write(f"Current Highest Bidder: {highest_bidder}")
        st.write(f"Highest Bid: {high_bid}")

#Button for making a bid
accounts = w3.eth.accounts
account = st.selectbox("Select which wallet to use", options=accounts)
teamId = st.selectbox("Which team are you bidding for?", range(len(team_list)), format_func=lambda x: team_list[x])
bidvalue = st.text_input("Bid Amount in Wei?")

if st.button("bid"):  
    contract.functions.bidForTeamId(int(teamId)).transact({"from": account, "value": bidvalue})

