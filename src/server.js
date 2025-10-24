const express = require("express");
const bodyParser = require("body-parser");
const sdkpCore = require("./sdkp_core");

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

app.get("/", (req, res) => {
  res.send("<h2>FatherTimeSDKP Engine is running</h2>");
});

app.post("/run-sdkp", async (req, res) => {
  const result = await sdkpCore.run(req.body);
  res.json(result);
});

app.listen(port, () => {
  console.log(`SDKP Engine listening on port ${port}`);
});
