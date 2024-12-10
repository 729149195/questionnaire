import express from 'express';
import cors from 'cors';

const app = express();
const port = 3000;

let submissionCount = 0;

app.use(cors({
  origin: 'http://localhost:5173' // Vite 默认开发服务器端口
}));
app.use(express.json());

// 获取当前计数
app.get('/api/count', (req, res) => {
  res.json({ count: submissionCount });
});

// 增加计数
app.post('/api/increment', (req, res) => {
  submissionCount++;
  res.json({ count: submissionCount });
});

// 重置计数
app.post('/api/reset', (req, res) => {
  submissionCount = 0;
  res.json({ count: submissionCount });
});

app.listen(port, () => {
  console.log(`Counter service running on port ${port}`);
}); 