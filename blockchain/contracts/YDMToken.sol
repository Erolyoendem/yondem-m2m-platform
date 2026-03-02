// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract YDMToken {
    string public name = "Yondem Token";
    string public symbol = "YDM";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    uint256 public constant MAX_SUPPLY = 100_000_000 * 10**18;
    uint256 public platformFee = 20;
    address public owner;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => bool) public minters;
    mapping(address => uint256) public stakedBalance;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event PlatformFeeUpdated(uint256 newFee);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier onlyMinter() {
        require(minters[msg.sender] || msg.sender == owner, "Not authorized");
        _;
    }
    
    constructor() {
        owner = msg.sender;
        _mint(msg.sender, 10_000_000 * 10**18);
    }
    
    function _mint(address to, uint256 amount) internal {
        require(totalSupply + amount <= MAX_SUPPLY, "Max supply exceeded");
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }
    
    function mint(address to, uint256 amount) external onlyMinter {
        _mint(to, amount);
    }
    
    function burn(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }
    
    function transfer(address to, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }
    
    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }
    
    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        require(balanceOf[from] >= amount, "Insufficient balance");
        require(allowance[from][msg.sender] >= amount, "Allowance exceeded");
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }
    
    function addMinter(address minter) external onlyOwner {
        minters[minter] = true;
    }
    
    function stake(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        stakedBalance[msg.sender] += amount;
        emit Staked(msg.sender, amount);
    }
    
    function unstake(uint256 amount) external {
        require(stakedBalance[msg.sender] >= amount, "Insufficient stake");
        stakedBalance[msg.sender] -= amount;
        balanceOf[msg.sender] += amount;
        emit Unstaked(msg.sender, amount);
    }
    
    function setPlatformFee(uint256 newFee) external onlyOwner {
        require(newFee <= 50, "Fee too high");
        platformFee = newFee;
        emit PlatformFeeUpdated(newFee);
    }
}
