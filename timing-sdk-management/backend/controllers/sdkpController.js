export const getSDKPState = (req, res) => {
  res.json({
    framework: "SDKP Quantum System",
    author: "FatherTimeSDKP",
    version: "1.0",
    description: "Unified SDKP-TimeSeal backend API endpoint"
  });
};
