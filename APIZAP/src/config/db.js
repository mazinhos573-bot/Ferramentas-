import { Pool } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

export const query = (text, params) => pool.query(text, params);

// Cria tabela se não existir
(async () => {
  try {
    await query(`
      CREATE TABLE IF NOT EXISTS contatos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100),
        telefone VARCHAR(20) UNIQUE NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS mensagens_enviadas (
        id SERIAL PRIMARY KEY,
        contato_id INTEGER REFERENCES contatos(id),
        conteudo TEXT NOT NULL,
        status VARCHAR(50),
        message_id VARCHAR(100),
        enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log('Tabelas verificadas/criadas com sucesso');
  } catch (err) {
    console.error('Erro ao criar tabelas:', err);
  }
})();