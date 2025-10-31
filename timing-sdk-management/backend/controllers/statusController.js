export const getStatus = (req, res) => {
  res.json({
    status: "ok",
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    time: new Date().toISOString()
  });
};
