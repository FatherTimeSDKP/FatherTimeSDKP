// upload-to-ipfs.js
// Usage: NFT_STORAGE_KEY=your_api_key node upload-to-ipfs.js
import fs from "fs";
import path from "path";
import { NFTStorage, File } from "nft.storage";

const apiKey = process.env.NFT_STORAGE_KEY;
if (!apiKey) {
  console.error("Set NFT_STORAGE_KEY env var to your nft.storage API key.");
  process.exit(1);
}

const client = new NFTStorage({ token: apiKey });

async function main() {
  const files = [
    "SC1-motor-specs.json",
    "SC1-motor-README.md",
    "SC1-motor-datasheet.pdf", // optional
    "SC1-motor-image.png" // optional
  ].filter(f => fs.existsSync(f)).map(f => new File([fs.readFileSync(f)], path.basename(f)));

  console.log("Uploading files to nft.storage...");
  const cid = await client.storeDirectory(files);
  console.log("Upload complete. Root CID:", cid);
  console.log("Example root gateway URL: https://ipfs.io/ipfs/" + cid);
  // Now create metadata JSON, update image/files URIs with this cid, then upload metadata and use its CID as tokenURI.
}

main().catch(console.error);
Install & run
