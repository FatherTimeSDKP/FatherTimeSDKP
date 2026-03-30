// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SC1Token is ERC721URIStorage, Ownable {
    uint256 private _nextTokenId = 1;
    mapping(uint256 => string) public eternalLedgerHash; // on-chain store

    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {}

    function mintWithLedger(address to, string memory tokenURI_, string memory ledgerHash_) external onlyOwner returns (uint256) {
        uint256 tokenId = _nextTokenId;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI_);
        eternalLedgerHash[tokenId] = ledgerHash_;
        _nextTokenId += 1;
        return tokenId;
    }

    // convenience getter already public via mapping variable
}
