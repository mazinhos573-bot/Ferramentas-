import { Router } from 'express';
import { enviarMensagem } from '../controllers/messageController.js';

const router = Router();

router.post('/enviar', enviarMensagem);

export default router;