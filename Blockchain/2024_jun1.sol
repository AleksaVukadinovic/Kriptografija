// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Auction {

    // a)

    struct AuctionItem {
        uint256 id;
        stirng name;
        uint256 minimalBid;
        uint256 currentHighestBid;
        address sellerAddress;
        bool ended;
    }

    // b)

    AuctionItem[] public items;

    // c)

    modifier onlyOwner() {
        require(msg.sender == owner, "Samo vlasnik moze pozvati ovu funkciju");
        _;
    }

     function addItem(string calldata _name, uint256 _minBid) external onlyOwner {
        uint256 newId = items.length;
        items.push(AuctionItem({
            id:            newId,
            name:          _name,
            minBid:        _minBid,
            highestBid:    0,
            highestBidder: address(0),
            ended:         false
        }));
    }

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // d)

    function endAuction(uint256 _itemId) external onlyOwner {
        AuctionItem item = items[_itemId];
        require(item.highestBid > 0, "Nema ponuda za ovaj predmet");

        item.ended = true;

        uint256 amount = item.highestBid;
        item.highestBid = 0;  // zastita od re-entrancy

        (bool success, ) = owner.call{value: amount}("");
        require(success, "Transfer vlasniku nije uspeo");
    }

    // e)

    mapping (address => uint256) public pendingReturns;

    // f)

    function bid(uint256 _itemId) external payable {
        require(_itemId < items.length, "Predmet ne postoji");
        AuctionItem storage item = items[_itemId];

        require(!item.ended,        "Aukcija je zavrsena");
        require(
            msg.value > item.minBid,
            "Ponuda mora biti veca od minimalne"
        );
        require(
            msg.value > item.highestBid,
            "Ponuda mora biti veca od trenutno nejvise"
        );

        // Registruj prethodnu ponudu za vracanje
        if (item.highestBidder != address(0)) {
            pendingReturns[item.highestBidder] += item.highestBid;
        }

        item.highestBid    = msg.value;
        item.highestBidder = msg.sender;

        emit HighestBidIncreased(_itemId, msg.sender, msg.value);
    }

    // g)

       event HighestBidIncreased(
        uint256 indexed itemId,
        address bidder,
        uint256 amount
    );

    // h)

    function withdraw() external returns (bool) {
        uint256 amount = pendingReturns[msg.sender];
        if (amount == 0) return false;

        // Nulirati pre slanja (zastita od re-entrancy)
        pendingReturns[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        if (!success) {
            pendingReturns[msg.sender] = amount;
            return false;
        }
        return true;
    }
}
