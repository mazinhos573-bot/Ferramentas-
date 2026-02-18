import axios from 'axios';
import dotenv from 'dotenv';
import { query } from '../config/db.js';

dotenv.config();

const PHONE_ID = process.env.WA_PHONE_NUMBER_ID;
const TOKEN = process.env.WA_ACCESS_TOKEN;
const VERSION = process.env.WA_VERSION || 'v21.0';

const API_URL = `https://graph.facebook.com/${VERSION}/${PHONE_ID}/messages`;

export const enviarMensagem = async (req, res) => {
  const { telefone, mensagem, nome } = req.body;

  if (!telefone || !mensagem) {
    return res.status(400).json({ error: 'telefone e mensagem são obrigatórios' });
  }

  const numeroLimpo = telefone.replace(/\D/g, '');
  const numeroWhats = numeroLimpo.startsWith('55') ? numeroLimpo : `55${numeroLimpo}`;

  try {
    // Salva ou busca contato
    let contatoResult = await query(
      'SELECT id FROM contatos WHERE telefone = $1',
      [numeroWhats]
    );

    let contatoId;
    if (contatoResult.rows.length === 0) {
      const novoContato = await query(
        'INSERT INTO contatos (nome, telefone) VALUES ($1, $2) RETURNING id',
        [nome || 'Sem nome', numeroWhats]
      );
      contatoId = novoContato.rows[0].id;
    } else {
      contatoId = contatoResult.rows[0].id;
    }

    // Envia mensagem via WhatsApp Cloud API (texto simples)
    const payload = {
      messaging_product: 'whatsapp',
      recipient_type: 'individual',
      to: numeroWhats,
      type: 'text',
      text: { preview_url: false, body: mensagem }
    };

    const response = await axios.post(API_URL, payload, {
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': 'application/json'
      }
    });

    const messageId = response.data.messages?.[0]?.id;

    // Salva no banco
    await query(
      'INSERT INTO mensagens_enviadas (contato_id, conteudo, status, message_id) VALUES ($1, $2, $3, $4)',
      [contatoId, mensagem, 'enviado', messageId]
    );

    return res.status(200).json({
      success: true,
      message: 'Mensagem enviada com sucesso',
      wa_message_id: messageId,
      contato: numeroWhats
    });

  } catch (error) {
    console.error('Erro ao enviar mensagem:', error.response?.data || error.message);

    const erroDetalhe = error.response?.data?.error?.message || error.message;

    // Salva tentativa falha (opcional)
    if (contatoId) {
      await query(
        'INSERT INTO mensagens_enviadas (contato_id, conteudo, status) VALUES ($1, $2, $3)',
        [contatoId, mensagem, `falha: ${erroDetalhe.slice(0, 200)}`]
      );
    }

    return res.status(500).json({
      success: false,
      error: erroDetalhe || 'Erro interno ao enviar mensagem'
    });
  }
};