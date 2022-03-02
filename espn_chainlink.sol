// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

/**
 * Request testnet LINK and ETH here: https://faucets.chain.link/
 * Find information on LINK Token Contracts and get the latest ETH and LINK faucets here: https://docs.chain.link/docs/link-token-contracts/
 */

/**
 * THIS IS AN EXAMPLE CONTRACT WHICH USES HARDCODED VALUES FOR CLARITY.
 * PLEASE DO NOT USE THIS CODE IN PRODUCTION.
 */
contract APIConsumer is ChainlinkClient {
    using Chainlink for Chainlink.Request;
  
    bytes32 public ncaaWinner;
    
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
    function getMarchMadnessWinner() public returns (bytes32 requestId) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        
        // Set the URL to perform the GET request on
        request.add("get", "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard");
        
        // Set the path to find the desired data in the API response, where the response format is:
        // {"RAW":
        //   {"ETH":
        //    {"USD":
        //     {
        //      "VOLUME24HOUR": xxx.xxx,
        //     }
        //    }
        //   }
        //  }

        // note from Ling - https://docs.chain.link/docs/jobs/task-types/jsonparse/ looks like v2 json parse can take the integers

        request.add("path", "events.0.competitions.0.competitors.0.team.shortDisplayName");
        request.add("path", "events.0.competitions.0.competitors.0.winner");
        request.add("path", "events.0.competitions.0.competitors.1.team.shortDisplayName");
        request.add("path", "events.0.competitions.0.competitors.1.winner");
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }
    
    /**
     * Receive the response in the form of bytes32=string
     */ 
    function fulfill(bytes32 _requestId, bytes32 _ncaaWinner) public recordChainlinkFulfillment(_requestId)
    {
        ncaaWinner = _ncaaWinner;
    }

    // function withdrawLink() external {} - Implement a withdraw function to avoid locking your LINK in the contract
}

