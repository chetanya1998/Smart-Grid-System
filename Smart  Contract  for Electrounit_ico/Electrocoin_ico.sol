//Electrocoins_ICO
pragma solidity ^0.4.11;
//number of coins issuing
contract electrocoins_ICO{
    //Introducing the maximum number of coins available
    uint256 public max_electrocoins = 1000000;

    //Introducing the Rs to electrocoins coversion rate
    uint public rs_to_electrocoins = 1000;

    // Introducing the total number of Electrocoins that have been bought by investors
    uint public total_electrocoins_bought=0;

    //Mapping from the investors address to its equity in Electrocoins and RS 
    mapping (address => uint)equity_electrocoins;
    mapping (address => uint)equity_rs;

    //checking if investor can buy Electrocoins
    modifier can_buy_electrocoins(uint rs_invested)
    {
        require(rs_invested * rs_to_electrocoins + total_electrocoins_bought <= max_electrocoins);
    _;

    }
    //getting the equity in electrocoins of an investor
    function equity_in_electrocoins(address investor)external constant returns(uint){
        return equity_electrocoins[investor];
    }


    //getting the equity in USD of an investor
      function equity_in_rs(address investor)external constant returns(uint){
        return equity_rs[investor];
    }

    //Buying electrocoins
    function buy_electrocoins(address investor, uint rs_invested)external
    can_buy_electrocoins(rs_invested){
        uint electrocoins_bought = rs_invested * rs_to_electrocoins;
        equity_electrocoins[investor] += electrocoins_bought;
        equity_rs[investor] =  equity_electrocoins[investor]/1000;
        total_electrocoins_bought += electrocoins_bought;


    }
    //selling electrocoins
      function sell_electrocoins(address investor, uint electrocoins_sold)external
    {  equity_electrocoins[investor] -= electrocoins_sold;
       equity_rs[investor] =  equity_electrocoins[investor]/1000;
       total_electrocoins_bought-=electrocoins_sold;
    }



}
