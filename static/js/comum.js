// Limpar o armazenamento local ao sair da página
window.addEventListener('beforeunload', function () {
    localStorage.removeItem('consultaData');
});
