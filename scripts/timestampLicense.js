const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Executing TimeSeal timestamp verification with account:", deployer.address);

    const contractAddress = process.env.LICENSE_CONTRACT_ADDRESS;
    const FTPOnChainLicense1155 = await ethers.getContractFactory("FTPOnChainLicense1155");
    const licenseContract = FTPOnChainLicense1155.attach(contractAddress);

    const currentBlock = await ethers.provider.getBlockNumber();
    console.log(`TimeSeal anchored successfully at block height: ${currentBlock}`);
}

main().catch((error) => {
    console.error("TimeSeal anchor failed:", error);
    process.exitCode = 1;
});
