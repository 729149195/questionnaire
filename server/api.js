const db = require('./db');

app.get('/api/count', async (req, res) => {
  const count = await db.getSubmissionCount();
  res.json({ count });
});

app.post('/api/count', async (req, res) => {
  const count = await db.incrementSubmissionCount();
  res.json({ count });
}); 