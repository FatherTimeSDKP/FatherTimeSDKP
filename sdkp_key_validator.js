
// SDKP-QCC Key Validator
// Author: Donald Paul Smith aka Father Time

function isValidSDKPKey(key) {
  const regex = /^sdkp-(11|12|19)-\d{4}-qcc-(\d{8})-([α-ζ])[a-f0-9]{12}$/;
  return regex.test(key);
}

function getKeyMetadata(key) {
  if (!isValidSDKPKey(key)) return null;

  const parts = key.split("-");
  return {
    scaleDomain: parts[1],
    collapseCode: parts[2],
    timestamp: parts[4],
    suffixHash: parts[5]
  };
}

// Example usage
const testKey = "sdkp-12-9999-qcc-20250601-ζ02b138be5b";
console.log("Valid Key?", isValidSDKPKey(testKey));
console.log("Metadata:", getKeyMetadata(testKey));
