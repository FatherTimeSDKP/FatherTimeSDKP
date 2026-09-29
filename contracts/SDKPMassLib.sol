// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SDKPMassLib
 * @dev Contains the SDKP mass calculation logic utilizing scale-density parameters.
 */
library SDKPMassLib {
    uint256 public constant SCALE_FACTOR = 1e18;

    function calculateMass(
        uint256 density,
        uint256 volume,
        uint256 velocityRotationFactor
    ) internal pure returns (uint256) {
        return (density * volume * velocityRotationFactor) / SCALE_FACTOR;
    }
}
