pragma solidity ^0.4.11;
contract auctioning{
    address payable beneficiary;
    uint32 public auctionStart;
    //Time for starting of bidding
    uint32 public biddingTime;
    //Minimum amount for bidding
    uint256 public min;
    //beneficiary power supply
    uint32 public power;
    //Time start for power supply
    uint32 public powerStart;
    //time stamp of supply end
    uint32 public powerEnd;
    //highest bidder
    address public highestBidder;
    //bidding amount of highest bid
    uint256 public highestBid;
    //state of auction(end==true)
    bool public ended;

    //deposit of bidders amount||return pending amount except bidding
    mapping(address=>uint)pendingReturns;

    function Auction(
        address _beneficiary,
        uint32  _auctionStart,
        uint32 _biddingTime,
        uint256 _min,
        uint32 _power,
        uint32 _powerStart,
        uint32 _powerEnd
        ) private{
            _beneficiary = _beneficiary;
            auctionStart = _auctionStart;
            _biddingTime = _biddingTime;
            min = _min;
            power =_power;
            powerStart =_powerStart;
            _powerEnd = _powerEnd;

        }
    function bid() public  payable{
        require(now < biddingTime);
        require(msg.value >= min);
        require(msg.value > highestBid);
        //fixing pre-bidding amount
        if(highestBid!=0){
            pendingReturns[highestBidder]+=highestBid;
        }
        //fix bidding amount
        highestBidder = msg.sender;
        highestBid = msg.value;

    }
    //if bidder wants to withdraw
    function Withdraw() public returns(bool){
       //freezed price
        require(ended == true);
       //bidder's total amount
       uint256 amount = pendingReturns[msg.sender];
       if(amount >0){
           pendingReturns[msg.sender] =amount;

        //withdraw unaccepted bidding amount
        if(!msg.sender.send(amount)){
            pendingReturns[msg.sender] =amount;
            return false;
        }
       }
       return true;

    }
    //end of auctionStart

    function Auctionend()public{
        //check the bidding time is over
        require(now >= biddingTime);
        //already end
        require(!ended);
        //set end
        ended =true;
        //transfer bidding amount to beneficiary
        beneficiary.transfer(highestBid);
        pendingReturns[highestBidder]-=highestBid;
    }

}
