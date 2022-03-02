import streamlit as st
import os
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

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
count = st_autorefresh(interval=1000)

st.title("March Madness Tournament!")
st.write("So you think you can pick the winner of this year's tourney? :sunglasses:")

#Logos and Geospatial representation csv file
teams = pd.read_csv(
    Path("./teams.csv"),
    index_col="school"
)

#Logo list
st.image([teams["logos"][0], teams["logos"][1], teams["logos"][2], teams["logos"][3], teams["logos"][4], teams["logos"][5], teams["logos"][6], teams["logos"][7], teams["logos"][8]], width=50)

#Map of Colleges
st.map(teams)


st.write("You can bid on each team that you think will win. Buyer of the winning team will win the entire pool.")

now = int(datetime.now().timestamp())
team_list = contract.functions.showTeamNames().call()

st.header("Dashboard")

st.write(f"The current teams in contention are: {team_list}")

#Dashboard Functions    
for i, team in enumerate(team_list):
    auction_result = contract.functions.auctionResult(i).call()
    auction_end_time = int(auction_result[0])
    highest_bidder = auction_result[1]
    high_bid = auction_result[2]
    st.write(f"Team Name: {team}")
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

st.sidebar.header("Make a Bid")
accounts = w3.eth.accounts
account = st.sidebar.selectbox("Select which wallet to use", options=accounts)
teamId = st.sidebar.selectbox("Which team are you bidding for?", range(len(team_list)), format_func=lambda x: team_list[x])
bidvalue = st.sidebar.text_input("Bid Amount in Wei?")

if st.sidebar.button("Make Bid"):  
    contract.functions.bidForTeamId(int(teamId)).transact({"from": account, "value": bidvalue})



