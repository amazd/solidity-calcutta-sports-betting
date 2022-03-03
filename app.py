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

st.image("mm.jpg")
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


st.write("You can bid on each team that you think will win.  Buyer of the winning team will win the entire pool!")

now = int(datetime.now().timestamp())
team_list = contract.functions.showTeamNames().call()

st.header("Dashboard")

st.write(f"The teams that are in the pool are:  {', '.join(team_list)}")

totalpot = 0

#Dashboard Functions    
for i, team in enumerate(team_list):
    auction_result = contract.functions.auctionResult(i).call()
    auction_end_time = int(auction_result[0])
    highest_bidder = auction_result[1]
    high_bid = w3.fromWei(int(auction_result[2]),'ether')
    totalpot = totalpot + high_bid
    st.subheader(f"Team Name: {team}")
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

st.subheader(f"The total pot is Ξ{round(totalpot,2)}!!")
        
#Button for making a bid

st.sidebar.header("Make a Bid")
accounts = w3.eth.accounts
newaccount={}
for account in accounts:
    accbal = round(w3.fromWei(w3.eth.get_balance(account),'ether'), 2)
    accbalstring = "(Ξ{balance}) {account}".format(balance = accbal, account = account)
    newaccount.update({account: accbalstring})
#account = st.sidebar.selectbox("Select which wallet to use", options=accounts)
account = st.sidebar.selectbox("Which wallet?", accounts, format_func=lambda x: newaccount[x])
teamId = st.sidebar.selectbox("Which team?", range(len(team_list)), format_func=lambda x: team_list[x])
bidvalue = w3.toWei(st.sidebar.number_input("Bid Amount in Eth"),'ether')

if st.sidebar.button("Make Bid"):  
    contract.functions.bidForTeamId(int(teamId)).transact({"from": account, "value": int(bidvalue)})

if st.sidebar.button("Reimburse for Losing Bids"):  
    contract.functions.withdrawLosingBidsForTeamId(int(teamId)).transact({"from": account})
    
if st.sidebar.button("Pay them their Money"):
    contract.functions.withdrawWinning().transact()

