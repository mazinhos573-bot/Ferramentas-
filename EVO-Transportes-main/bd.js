import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js';
import { getDatabase, ref, get, set, child, push, onValue, update, remove, serverTimestamp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js';

const firebaseConfig = {
  apiKey: 'AIzaSyCPoCn98zQYHhsQp7oYyYC3p6pejLyCKdk',
  authDomain: 'tough-messenger-467220-h2.firebaseapp.com',
  databaseURL: 'https://tough-messenger-467220-h2-default-rtdb.firebaseio.com',
  projectId: 'tough-messenger-467220-h2',
  storageBucket: 'tough-messenger-467220-h2.firebasestorage.app',
  messagingSenderId: '797984737364',
  appId: '1:797984737364:web:7c9cf10ca4169e581f45c1'
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

const initDatabase = async () => {
  const dbRef = ref(db);
  try {
    const snapshot = await get(child(dbRef, 'users/EricLM'));
    if (!snapshot.exists()) {
      await set(ref(db, 'users/EricLM'), {
        password: 'Evo@537361',
        role: 'admin',
        avatar: 'https://ui-avatars.com/api/?name=Eric+LM&background=4f46e5&color=fff',
        createdAt: serverTimestamp()
      });
      console.log('✅ Usuário ADM criado com sucesso.');
    }
  } catch (error) {
    console.error('Erro ao inicializar banco:', error);
  }
};

initDatabase();

export { db, ref, get, set, child, push, onValue, update, remove, serverTimestamp };