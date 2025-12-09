// scripts/deploy-and-mint.js
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const SC1 = await hre.ethers.getContractFactory("SC1Token");
  const sc1 = await SC1.deploy("SC1 Motor Specs", "SC1");
  await sc1.deployed();
  console.log("SC1Token deployed to:", sc1.address);

  // Replace with recipient address and metadata tokenURI (ipfs://<metadataCID>)
  const recipient = "REPLACE_WITH_RECIPIENT_ADDRESS";
  const tokenURI = "ipfs://REPLACE_WITH_METADATA_CID";

  const tx = await sc1.mint(recipient, tokenURI);
  console.log("Mint tx hash:", tx.hash);
  await tx.wait();
  console.log("Minted token to", recipient);
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
