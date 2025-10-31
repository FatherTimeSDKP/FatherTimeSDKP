const qcc0 = require("./modules/qcc0");
const sdvr = require("./modules/sdvr");
const llal = require("./modules/llal");

module.exports = {
  run: async (input) => {
    const qccResult = qcc0.process(input);
    const sdvrResult = sdvr.calculate(qccResult);
    const llalResult = llal.loop(qccResult, sdvrResult);
    
    return {
      input,
      qccResult,
      sdvrResult,
      llalResult,
      timestamp: new Date().toISOString()
    };
  }
};
