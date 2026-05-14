import { db, ref, push, onValue, serverTimestamp } from './bd.js';

export function initChat(currentUser, containerId, roomName = 'geral') {
  const container = document.getElementById(containerId);
  if (!container) return;

  let activeRoom = 'global';

  window.mentionUser = (username) => {
    const input = document.getElementById('chat-input');
    if (input) {
      input.value = `@${username} ${input.value}`;
      input.focus();
    }
  };

  const renderBase = () => {
    container.innerHTML = `
      <div class="flex flex-col h-full bg-white border-l border-gray-200 shadow-xl">
        <div class="p-4 border-b border-gray-100 bg-slate-50 flex flex-col gap-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-comments text-indigo-600"></i>
              <h3 class="font-semibold text-slate-800">Chat de Operações</h3>
            </div>
          </div>
          <div class="flex bg-gray-200 p-1 rounded-lg text-xs font-medium">
            <button id="btn-room-global" class="flex-1 py-1.5 rounded-md transition-all ${activeRoom === 'global' ? 'bg-white shadow text-indigo-600' : 'text-gray-500'}">Global</button>
            <button id="btn-room-local" class="flex-1 py-1.5 rounded-md transition-all ${activeRoom !== 'global' ? 'bg-white shadow text-indigo-600' : 'text-gray-500'}">Setor: ${roomName}</button>
          </div>
        </div>
        <div id="chat-messages" class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/50"></div>
        <div class="p-4 bg-white border-t border-gray-100">
          <form id="chat-form" class="flex gap-2">
            <input type="text" id="chat-input" class="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm" placeholder="Mensagem..." autocomplete="off" required>
            <button type="submit" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">
              <i class="fa-solid fa-paper-plane"></i>
            </button>
          </form>
        </div>
      </div>
    `;

    setupEventListeners();
    listenMessages();
  };

  const setupEventListeners = () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const btnGlobal = document.getElementById('btn-room-global');
    const btnLocal = document.getElementById('btn-room-local');

    chatForm.onsubmit = async (e) => {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (!text) return;

      await push(ref(db, `chat/${activeRoom}`), {
        sender: currentUser.username,
        role: currentUser.role,
        avatar: currentUser.avatar || `https://ui-avatars.com/api/?name=${currentUser.username}`,
        text: text,
        timestamp: serverTimestamp()
      });
      chatInput.value = '';
    };

    btnGlobal.onclick = () => { activeRoom = 'global'; renderBase(); };
    btnLocal.onclick = () => { activeRoom = roomName; renderBase(); };
  };

  let unsubscribe = null;
  const listenMessages = () => {
    if (unsubscribe) unsubscribe();
    const messagesDiv = document.getElementById('chat-messages');
    
    onValue(ref(db, `chat/${activeRoom}`), (snapshot) => {
      messagesDiv.innerHTML = '';
      const data = snapshot.val();
      if (!data) return;

      Object.values(data).sort((a, b) => a.timestamp - b.timestamp).forEach(msg => {
        const isMe = msg.sender === currentUser.username;
        let safeText = msg.text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        
        const mentionRegex = /@(\w+)/g;
        const isMentioned = safeText.includes(`@${currentUser.username}`);
        safeText = safeText.replace(mentionRegex, '<span class="text-indigo-600 font-bold bg-indigo-50 px-1 rounded">@$1</span>');

        const msgElement = document.createElement('div');
        msgElement.className = `flex gap-2 ${isMe ? 'flex-row-reverse' : 'flex-row'} ${isMentioned ? 'ring-2 ring-yellow-400 p-1 rounded-lg bg-yellow-50' : ''}`;
        
        msgElement.innerHTML = `
          <img src="${msg.avatar}" class="w-8 h-8 rounded-full border border-gray-200">
          <div class="flex flex-col ${isMe ? 'items-end' : 'items-start'}">
            <span onclick="window.mentionUser('${msg.sender}')" class="text-[10px] text-gray-500 mb-1 cursor-pointer hover:text-indigo-600">
              ${msg.sender} (${msg.role})
            </span>
            <div class="px-4 py-2 rounded-2xl max-w-[200px] break-words text-sm ${isMe ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-white text-gray-800 border border-gray-200 rounded-tl-none'}">
              ${safeText}
            </div>
          </div>
        `;
        messagesDiv.appendChild(msgElement);
      });
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
  };

  renderBase();
}