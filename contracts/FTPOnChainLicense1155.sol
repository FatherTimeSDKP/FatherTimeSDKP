// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./SDKPMassLib.sol";

/**
 * @title FTPOnChainLicense1155
 * @dev ERC-1155 license contract with embedded parameters and real-time SDKP mass calculations.
 */
contract FTPOnChainLicense1155 is ERC1155, Ownable {
    using SDKPMassLib for uint256;

    mapping(uint256 => uint256) public tokenDensity;
    mapping(uint256 => uint256) public tokenVolume;
    mapping(uint256 => uint256) public tokenVRF;

    constructor() ERC1155("") Ownable(msg.sender) {}

    function mintLicense(
        address account,
        uint256 id,
        uint256 density,
        uint256 volume,
        uint256 vrf,
        bytes memory data
    ) public onlyOwner {
        tokenDensity[id] = density;
        tokenVolume[id] = volume;
        tokenVRF[id] = vrf;
        _mint(account, id, 1, data);
    }

    function getCalculatedMass(uint256 id) public view returns (uint256) {
        return SDKPMassLib.calculateMass(tokenDensity[id], tokenVolume[id], tokenVRF[id]);
    }
}
