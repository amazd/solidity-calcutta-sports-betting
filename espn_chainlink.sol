// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

/**
 * Request testnet LINK and ETH here: https://faucets.chain.link/
 * Find information on LINK Token Contracts and get the latest ETH and LINK faucets here: https://docs.chain.link/docs/link-token-contracts/
 */

contract APIConsumer is ChainlinkClient {
    using Chainlink for Chainlink.Request;
  
    bytes32 public isTeamOneWinner;
    bytes32 public teamOne;
    bytes32 public teamTwo;

    address private oracle;
    bytes32 private jobId;
    uint256 private fee;
    
    /**
     * Network: Kovan
     * Oracle: 0xc57B33452b4F7BB189bB5AfaE9cc4aBa1f7a4FD8 (Chainlink Devrel   
     * Node)
     * Job ID: d5270d1c311941d0b08bead21fea7747
     * Fee: 0.1 LINK
     */
    constructor() {
        setPublicChainlinkToken();
        oracle = 0xc57B33452b4F7BB189bB5AfaE9cc4aBa1f7a4FD8;
        jobId = "d5270d1c311941d0b08bead21fea7747";
        fee = 0.1 * 10 ** 18; // (Varies by network and job)
    }
    
    /**
     * Create a Chainlink request to retrieve API response, find the target
     */

    function getIsTeamOneWinner() public returns (bytes32 requestId1) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfillWinner.selector);
        
        // Set the URL to perform the GET request on
        request.add("get", "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard");
        
        // Set the path to find the desired data in the API response, where the response format is:

        request.add("path", "events[0].competitions[0].competitors[0].winner");
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }
    
    function getTeamOne() public returns (bytes32 requestId2) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfillTeamOne.selector);
        
        // Set the URL to perform the GET request on
        request.add("get", "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard");
        
        // Set the path to find the desired data in the API response, where the response format is:

        request.add("path", "events[0].competitions[0].competitors[0].team.shortDisplayName");

        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }

    function getTeamTwo() public returns (bytes32 requestId3) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfillTeamTwo.selector);
        
        // Set the URL to perform the GET request on
        request.add("get", "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard");
        
        // Set the path to find the desired data in the API response, where the response format is:
        request.add("path", "events[0].competitions[0].competitors[1].team.shortDisplayName");
        
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }

    /**
     * Receive the response 
     */ 
    function fulfillWinner(bytes32 _requestId1, bytes32 _isTeamOneWinner) public recordChainlinkFulfillment(_requestId1)
    {
        isTeamOneWinner = _isTeamOneWinner;
    }


    function fulfillTeamOne(bytes32 _requestId2, bytes32 _teamOne) public recordChainlinkFulfillment(_requestId2)
    {
        teamOne = _teamOne;
    }

    function fulfillTeamTwo(bytes32 _requestId3, bytes32 _teamTwo) public recordChainlinkFulfillment(_requestId3)
    {
        teamTwo = _teamTwo;
    }
    // function withdrawLink() external {} - Implement a withdraw function to avoid locking your LINK in the contract
}

