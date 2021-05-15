// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;
pragma solidity 0.8.4;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface DaoInterface {
    enum Vote {Yes, No}
    enum Status {Pending, Approved, Rejected}

    struct Proposal {
        address creator;
        bytes32 docHash;
        uint256 creationTimestamp;
        uint256 yea;
        uint256 nay;
        Status status;
    }

    function deposit(uint256 _amount) external;

    function withdraw(uint256 _amount) external;

    function newProposal(bytes32 _proposalHash) external;

    function vote(bytes32 _proposalHash, Vote _vote) external;

    event Approved(bytes32 _proposalHash);
    event ProposalCreated(bytes32 _proposalHash);
    event Rejected(bytes32 _proposalHash);
    event VoteEvent(address _account, Vote vote);
}

contract Dao is DaoInterface {
    IERC20 public token;
    uint256 public totalShares;
    uint256 constant quorumPeriod = 1 weeks;
    uint256 constant quorumPercentage = 50;

    mapping(bytes32 => Proposal) public proposals;
    bytes32[] proposalHashes;
    mapping(address => mapping(bytes32 => bool)) public voted;
    mapping(address => uint256) public shares;

    constructor(address _token) {
        token = IERC20(_token);
    }

    // Modifiers
    modifier proposalNotExists(bytes32 _proposalHash) {
        require(
            proposals[_proposalHash].docHash == bytes32(0),
            "this proposal already exist"
        );
        _;
    }

    modifier proposalExists(bytes32 _proposalHash) {
        require(
            proposals[_proposalHash].docHash != bytes32(0),
            "this proposal does not exist"
        );
        _;
    }

    modifier accountHasEnoughShares(uint256 _amount) {
        require(shares[msg.sender] >= _amount, "not enough shares");
        _;
    }

    modifier accountNotVoted(bytes32 _proposalHash) {
        require(voted[msg.sender][_proposalHash] == false, "already voted");
        _;
    }

    modifier inVotingPeriod(bytes32 _proposalHash) {
        require(
            block.timestamp <=
                proposals[_proposalHash].creationTimestamp + quorumPeriod,
            "voting period over"
        );
        _;
    }

    // Functions
    function deposit(uint256 _amount) external override {
        shares[msg.sender] += _amount;
        totalShares += _amount;
        token.transferFrom(msg.sender, address(this), _amount);
    }

    function withdraw(uint256 _amount)
        external
        override
        accountHasEnoughShares(_amount)
    {
        shares[msg.sender] -= _amount;
        totalShares -= _amount;
        token.transfer(msg.sender, _amount);
    }

    function newProposal(bytes32 _proposalHash)
        external
        override
        proposalNotExists(_proposalHash)
    {
        proposalHashes.push(_proposalHash);
        proposals[_proposalHash] = Proposal(
            msg.sender,
            _proposalHash,
            block.timestamp,
            0,
            0,
            Status.Pending
        );

        emit ProposalCreated(_proposalHash);
    }

    function vote(bytes32 _proposalHash, Vote _vote)
        external
        override
        accountNotVoted(_proposalHash)
        proposalExists(_proposalHash)
    {
        Proposal storage proposal = proposals[_proposalHash];

        voted[msg.sender][_proposalHash] = true;
        if (_vote == Vote.Yes) {
            proposal.yea += shares[msg.sender];
            emit VoteEvent(msg.sender, _vote);

            if ((proposal.yea * 100) / totalShares > quorumPercentage) {
                proposal.status = Status.Approved;
                emit Approved(_proposalHash);
            }
        } else {
            proposal.nay += shares[msg.sender];
            if ((proposal.nay * 100) / totalShares > quorumPercentage) {
                proposal.status = Status.Rejected;
                emit Rejected(_proposalHash);
            }
        }
    }

    function getProposalHashes() public view returns (bytes32[] memory) {
        return proposalHashes;
    }

    function getProposalCount() public view returns (uint256) {
        return proposalHashes.length;
    }

    function getProposal(bytes32 _proposalHash)
        public
        view
        returns (
            address creator,
            bytes32 docHash,
            uint256 creationTimestamp,
            uint256 yea,
            uint256 nay,
            Status status
        )
    {
        Proposal storage proposal = proposals[_proposalHash];

        return (
            proposal.creator,
            proposal.docHash,
            proposal.creationTimestamp,
            proposal.yea,
            proposal.nay,
            proposal.status
        );
    }
}
