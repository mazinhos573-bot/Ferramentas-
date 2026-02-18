import express from 'express';
import dotenv from 'dotenv';
import messageRoutes from './routes/messages.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/health', (req, res) => res.json({ status: 'API WhatsApp Banda rodando!' }));

app.use('/api/mensagens', messageRoutes);

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
  console.log(`POST /api/mensagens/enviar  →  envie mensagens`);
});