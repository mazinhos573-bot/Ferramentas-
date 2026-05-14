# Documentação Técnica - EVO Transportes

## Estrutura de Arquivos
- `bd.js`: Configuração do Firebase e exportação de métodos de banco.
- `auth.js`: Lógica de proteção de rotas e persistência de sessão.
- `chat.js`: Componente reutilizável de chat (Global e Setorial).
- `index.html`: Portal de entrada e lógica de login.
- `motorista.html`: Interface simplificada para registro de dados.
- `portaria.html`: Módulo de recepção e triagem.
- `gerenciamento.html`: Dashboard master para controle total e criação de usuários.
- `visualizacao.html`: Painel passivo para monitoramento de KPIs.

## Hierarquia de Acesso (Roles)
1. **admin**: Acesso total a todas as páginas e ferramentas de limpeza de chat/banimento.
2. **portaria**: Acesso ao painel de liberação e chat.
3. **motorista**: Acesso ao formulário de entrada e chat.
4. **visualizacao**: Acesso restrito ao painel de monitoramento e KPIs.

## Fluxo de Dados
1. Motorista submete formulário -> `transportes/` (status: `aguardando_portaria`).
2. Portaria libera entrada -> Status muda para `aguardando_descarga`.
3. Admin inicia descarga -> Status muda para `descarga_em_andamento`.
4. Admin finaliza/libera -> Status muda para `descarga_finalizada` / `liberado`.