export function checkAuth(requiredRole = null) {
  const userStr = localStorage.getItem('evo_user');
  if (!userStr) {
    window.location.href = 'index.html';
    return null;
  }

  const user = JSON.parse(userStr);

  if (user.banned) {
    alert("Sua conta foi desativada.");
    logout();
    return null;
  }

  if (requiredRole && requiredRole !== 'any') {
    if (requiredRole === 'admin' && user.role !== 'admin') {
      window.location.href = 'index.html';
    }
    if (requiredRole === 'portaria' && !['portaria', 'admin'].includes(user.role)) {
      window.location.href = 'index.html';
    }
    if (requiredRole === 'motorista' && !['motorista', 'admin'].includes(user.role)) {
      window.location.href = 'index.html';
    }
    if (requiredRole === 'visualizacao' && !['visualizacao', 'admin'].includes(user.role)) {
      window.location.href = 'index.html';
    }
  }

  return user;
}

export function logout() {
  localStorage.removeItem('evo_user');
  window.location.href = 'index.html';
}