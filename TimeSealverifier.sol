// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

/// @title TimeSealVerifier - On-chain license/content timestamping contract
/// @author FatherTimeSDKP
/// @notice Allows anyone to register a one-time timestamp for any content hash (e.g. license document hash)
contract TimeSealVerifier {
    // Mapping from license/content hash to timestamp
    mapping(bytes32 => uint256) private _timestamps;

    // Event emitted when a license hash is timestamped
    event LicenseTimestamped(bytes32 indexed licenseHash, uint256 timestamp);

    /// @notice Record a timestamp for the given license/content hash
    /// @dev Can only be called once per unique licenseHash
    /// @param licenseHash The keccak256 hash of the license or content to timestamp
    function timestampLicense(bytes32 licenseHash) external {
        require(licenseHash != bytes32(0), "TimeSealVerifier: invalid hash");
        require(_timestamps[licenseHash] == 0, "TimeSealVerifier: already timestamped");

        uint256 currentTime = block.timestamp;
        _timestamps[licenseHash] = currentTime;

        emit LicenseTimestamped(licenseHash, currentTime);
    }

    /// @notice Check if a license hash has been timestamped
    /// @param licenseHash The license/content hash to query
    /// @return True if timestamped, false otherwise
    function isTimeSealed(bytes32 licenseHash) external view returns (bool) {
        return _timestamps[licenseHash] != 0;
    }

    /// @notice Get the timestamp for a license hash
    /// @param licenseHash The license/content hash to query
    /// @return The UNIX timestamp of when the license was timestamped (0 if never)
    function getTimestamp(bytes32 licenseHash) external view returns (uint256) {
        return _timestamps[licenseHash];
    }
}
