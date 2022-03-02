pragma solidity>=0.7.0 <0.9.0;

contract Auction{

    struct auctionInfo {
        mapping(address => uint) pendingBids; // list of how much each wallet has bid, so we can refund
        uint auctionEndTime;
        address highestBidder;
        uint highestbid;
        bool ended;
    }

    mapping(uint => auctionInfo) public auctionResult; // bid information per team id
    
    string[] public teamNames;
    address public contractOwner;
    bool WinningPaidOut;

    event highestBidIncreased(address bidder, uint amount);
    event auctionEnded(address winner, uint amount);
    event winningPaidOut(address winner, uint amount);

    uint constant secondsPerAuction = 2*60; // 2 min minutes after the fist bid per auction id

    constructor() public {
        contractOwner = msg.sender;
        WinningPaidOut = false;
    }

    function addTeamName(string memory _name) public {
        teamNames.push(_name);
    }

    // could this be made so it's free to access 
    function showTeamNames() public returns(string[] memory) {
        return teamNames;  
    }

    modifier onlyOwner() {
        require(msg.sender == contractOwner);
        _;
    }

    function auctionHasNotEndedForTeamId(uint _teamId) public returns(bool) {
        if(block.timestamp > auctionResult[_teamId].auctionEndTime) {
            auctionResult[_teamId].ended = true;
            emit auctionEnded(auctionResult[_teamId].highestBidder, auctionResult[_teamId].highestbid);
        }
        return !auctionResult[_teamId].ended;
    }

    function bidForTeamId(uint _teamId) public payable {
        if(auctionResult[_teamId].auctionEndTime == 0) { // start the auction time
            auctionResult[_teamId].auctionEndTime = block.timestamp + secondsPerAuction;
        }

        require(auctionHasNotEndedForTeamId(_teamId), "The Auction Time Is Over");

        if(msg.value > auctionResult[_teamId].highestbid) {

            // if sender has alreadybid, we refund the amount they already sent before recording their new bid
            if(auctionResult[_teamId].pendingBids[msg.sender] > 0)
            {
                uint amount = auctionResult[_teamId].pendingBids[msg.sender];
                payable(msg.sender).transfer(amount);
            }

            auctionResult[_teamId].pendingBids[msg.sender] = msg.value;
            auctionResult[_teamId].highestBidder = msg.sender;
            auctionResult[_teamId].highestbid = msg.value;

            emit highestBidIncreased(msg.sender, msg.value);
        }
        else {
            revert("Sorry, the bid needs to be higher than the current winning bid!");
        }
     }

    // after an auction is over, losers can ask to withdraw their losing bid amounts back
    function withdrawLosingBidsForTeamId(uint _teamId) public payable returns(bool) {
        require(!auctionHasNotEndedForTeamId(_teamId), "You Cannot Withdraw Until The Auction Has Ended");
        require(auctionResult[_teamId].highestBidder != msg.sender, "Highest bidder for an auction can not withdraw");
        
        uint amount = auctionResult[_teamId].pendingBids[msg.sender];
        if(amount > 0) {
            auctionResult[_teamId].pendingBids[msg.sender] = 0;
        }
        
        if(!payable(msg.sender).send(amount)) {
            auctionResult[_teamId].pendingBids[msg.sender] = amount;
        }
        return true;
    }

    function withdrawWinning() public onlyOwner returns(bool) {
        require(!WinningPaidOut, "Winnings already paid out");

        string memory winningTeamName = "Baylor";
        
        uint winningTeamId;
        uint totalPotAmount = 0;

        for (uint i=0; i < teamNames.length; i++) {
            require(!auctionHasNotEndedForTeamId(i), "At least one of the auctions is not over yet");

            totalPotAmount += auctionResult[i].highestbid;
            if(stringsAreEqual(winningTeamName, teamNames[i])){
                winningTeamId = i;
            } 
        }

        address winningWallet = auctionResult[winningTeamId].highestBidder;
        WinningPaidOut = true;

        if(!payable(winningWallet).send(totalPotAmount)) {
            WinningPaidOut = false;
        }

        emit winningPaidOut(winningWallet, totalPotAmount);

        return true;
    }

    function stringsAreEqual(string memory a, string memory b) private view returns (bool) {
        return (keccak256(bytes(a)) == keccak256(bytes(b)));
    }

}