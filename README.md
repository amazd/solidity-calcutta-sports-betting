# March MadnETH 
## Calcutta Betting with Smart Contracts
!![This is an image](https://images.rivals.com/image/upload/f_auto,q_auto,t_large/v0wuctkikgvrerd2pbdg)
## Table of Contents:
####
- Project Overview
- What is a Calcutta?
- March MadnETH Calcutta rules
- How to use the App
- Technologies
---
## Project Overview
### Project Goal:
####
- Create a novel sports betting app using the interactive features in the Steamlit GUI
- Deploy smart contracts to the ETH blockchain for wagering and payout utilities
- Write contract in Solidity through the use of Remix IDE
- Users can bid on auctions in a Calcutta betting pool


## What is a Calcutta?
####
- In sports betting, a Calcutta is analogous to an open auction
- Calcuttas are popular in sports with non-binary outcomes and/or a large number of contestants.  Examples include:
    - Horse racing
    - Golf tournaments
    - The NCAA Tournament
- We chose a Calcutta format to create a web-hosted sports betting application that is both interactive with blockchain, and is the first of its kind (as far as we can tell)

## March MadnETH Calcutta Rules
####
- Fixed and uniform buy-in in ETH
- Teams are auctioned off in random order
- Each bidding period has a time limit; this is currently set at 120 seconds for demo purposes

## Installation Guide

Install streamlit through the command **pip install streamlit**
Install streamlit_autorefresh through the command **pip install streamlit_autorefresh**
Install web3 through the command **pip install web3==5.17**
Install os through the command **pip install os_sys**


## Technologies
##### The following Python libraries were imported
```
# Import the required libraries and dependencies
import streamlit as st
import os
import json
import pandas as pd
import numpy as np
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
```

Remix IDE was also used for the smart contract development.  The website is **https://remix.ethereum.org**

## App usage:
```mermaid
sequenceDiagram
```

## How to enter the pool and use The App
####
- Step 1: Update Smart contract address and web3 provider in API.env file and then type **streamlit run app.py** in a terminal
- Step 2: Once an auction starts, the dashboard will display 3 items:
    - Time remaining
    - Winning Bidder
    - Highest Bid
- Each participant will have the opportunity to submit higher bids until time runs out
- For a starting bid, the participant will deposit money into the contract mapped to the selected team
- For a follow-on bid, the participant will deposit additional money into the contract
- After time runs out, the contract will no longer accept bids and the winning bidder will be displayed on the dashboard
- Losing bids will be refunded upon auction close through clicking a single button
- Total pot size will be displayed at the bottom of the dashboard

## Content

Here are some images that illustrate how the Calcutta works:

API.env file example:

![API Example](Images/APIExample.PNG)

Sidebar with buttons for bid, reclaiming losing bids, giving pot to winner:

![Sidebar](Images/Sidebar.PNG)

Teams In Pool:

![Graphics](Images/TeamsInPool.PNG)

Arizona Auction Winner:

![Graphics](Images/ArizonaAuction.PNG)

Auction In Progress:

![Graphics](Images/PurdueAuctionInProgress.PNG)

Pot Size:

![Pot Size](Images/PotSize.PNG)


## Contributors
Ahmad Sadraei, asadraei@gmail.com
Vishnu Kurella, vishnu.kurella@gmail.com
Lee Copeland, lcopeland44@gmail.com
Ling Zhou,lzhou1688@gmail.com

## License
Blitz.LQA 2021