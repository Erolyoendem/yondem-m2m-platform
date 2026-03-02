// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IYDMToken {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract PublisherContract {
    struct Deal {
        address publisher;
        address advertiser;
        uint256 productId;
        uint256 amount;
        uint256 commission;
        bool executed;
        uint256 timestamp;
    }
    
    IYDMToken public ydmToken;
    mapping(uint256 => Deal) public deals;
    mapping(address => uint256) public trustScore;
    mapping(address => bool) public authorizedAgents;
    
    uint256 public dealCounter;
    uint256 public platformFeePercent = 20;
    address public platformWallet;
    
    event DealCreated(uint256 indexed dealId, address publisher, address advertiser);
    event DealExecuted(uint256 indexed dealId, uint256 commission);
    event TrustScoreUpdated(address indexed agent, uint256 newScore);
    
    modifier onlyAuthorized() {
        require(authorizedAgents[msg.sender] || msg.sender == platformWallet, "Not authorized");
        _;
    }
    
    constructor(address _ydmToken, address _platformWallet) {
        ydmToken = IYDMToken(_ydmToken);
        platformWallet = _platformWallet;
        authorizedAgents[msg.sender] = true;
    }
    
    function createDeal(address _publisher, address _advertiser, uint256 _productId, uint256 _amount, uint256 _commission) external onlyAuthorized returns (uint256) {
        dealCounter++;
        deals[dealCounter] = Deal({
            publisher: _publisher,
            advertiser: _advertiser,
            productId: _productId,
            amount: _amount,
            commission: _commission,
            executed: false,
            timestamp: block.timestamp
        });
        emit DealCreated(dealCounter, _publisher, _advertiser);
        return dealCounter;
    }
    
    function executeDeal(uint256 _dealId) external onlyAuthorized {
        Deal storage deal = deals[_dealId];
        require(!deal.executed, "Already executed");
        require(ydmToken.balanceOf(deal.advertiser) >= deal.commission, "Insufficient advertiser balance");
        
        uint256 platformFee = (deal.commission * platformFeePercent) / 100;
        uint256 publisherReward = deal.commission - platformFee;
        
        ydmToken.transferFrom(deal.advertiser, platformWallet, platformFee);
        ydmToken.transferFrom(deal.advertiser, deal.publisher, publisherReward);
        
        deal.executed = true;
        updateTrustScore(deal.publisher, true);
        emit DealExecuted(_dealId, deal.commission);
    }
    
    function updateTrustScore(address _agent, bool success) internal {
        if (success) {
            trustScore[_agent] = trustScore[_agent] + 1 > 100 ? 100 : trustScore[_agent] + 1;
        } else {
            trustScore[_agent] = trustScore[_agent] > 0 ? trustScore[_agent] - 1 : 0;
        }
        emit TrustScoreUpdated(_agent, trustScore[_agent]);
    }
    
    function setAuthorizedAgent(address _agent, bool _status) external {
        require(msg.sender == platformWallet, "Only platform");
        authorizedAgents[_agent] = _status;
    }
}
