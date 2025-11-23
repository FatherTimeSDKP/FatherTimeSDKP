export const getData = (req, res) => {
  res.json({ message: 'Data fetched successfully', timestamp: Date.now() });
};

export const postData = (req, res) => {
  const body = req.body;
  res.json({ message: 'Data received', received: body });
};
