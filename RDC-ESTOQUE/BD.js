// BD.js
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.14.0/firebase-app.js';
import { getDatabase, ref, push, update, onValue, remove, set, get } from 'https://www.gstatic.com/firebasejs/10.14.0/firebase-database.js';

// Configuração do Seu Firebase
const firebaseConfig = {
  apiKey: "AIzaSyDTr6hR8jwGONeDRXa_8vPShBkw0mJVceM",
  authDomain: "contole-de-estoque-cdc.firebaseapp.com",
  databaseURL: "https://contole-de-estoque-cdc-default-rtdb.firebaseio.com",
  projectId: "contole-de-estoque-cdc",
  storageBucket: "contole-de-estoque-cdc.firebasestorage.app",
  messagingSenderId: "11141306715",
  appId: "1:11141306715:web:c3294ca3c337f5a01ea27e",
  measurementId: "G-WR3NG9LX8C"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

// Exportar
export { database, ref, push, update, onValue, remove, set, get };