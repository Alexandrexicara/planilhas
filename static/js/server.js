// Server.js - Configuração global para templates

// Configuração da API
const API_CONFIG = {
    baseURL: window.location.origin,
    timeout: 10000
};

// Funções globais de autenticação
window.AuthAPI = {
    // Login
    async login(email, senha, next = '') {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('senha', senha);
        formData.append('next', next);

        try {
            console.log('=== AuthAPI Login ===');
            console.log('Enviando para:', `${API_CONFIG.baseURL}/login`);
            console.log('FormData entries:');
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }

            const response = await fetch(`${API_CONFIG.baseURL}/login`, {
                method: 'POST',
                body: formData,
                timeout: API_CONFIG.timeout
            });

            console.log('Response status:', response.status);
            const responseText = await response.text();
            console.log('Response text:', responseText);

            const data = JSON.parse(responseText);
            return data;
        } catch (error) {
            console.error('Erro no login:', error);
            return { success: false, message: 'Erro de conexão' };
        }
    },

    // Registro
    async register(formData) {
        try {
            console.log('=== AuthAPI Register ===');
            console.log('Enviando para:', `${API_CONFIG.baseURL}/registro`);
            console.log('FormData:', Array.from(formData.entries()));

            const response = await fetch(`${API_CONFIG.baseURL}/registro`, {
                method: 'POST',
                body: formData,
                timeout: API_CONFIG.timeout
            });

            console.log('Response status:', response.status);
            const responseText = await response.text();
            console.log('Response text:', responseText);

            const data = JSON.parse(responseText);
            return data;
        } catch (error) {
            console.error('Erro no registro:', error);
            return { success: false, message: 'Erro de conexão' };
        }
    }
};

// Funções utilitárias
window.Utils = {
    // Mostrar mensagem de status
    showStatus(message, type = 'info', duration = 5000) {
        const statusDiv = document.getElementById('statusMessage');
        const statusText = document.getElementById('statusText');
        
        if (statusDiv && statusText) {
            statusDiv.className = `alert alert-${type} alert-dismissible fade show`;
            statusText.textContent = message;
            statusDiv.style.display = 'block';
            
            if (duration > 0) {
                setTimeout(() => {
                    statusDiv.style.display = 'none';
                }, duration);
            }
        }
    },

    // Validar email
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Validar senha
    isValidPassword(senha) {
        return senha && senha.length >= 6;
    },

    // Redirecionar
    redirect(url, delay = 0) {
        if (delay > 0) {
            setTimeout(() => {
                window.location.href = url;
            }, delay);
        } else {
            window.location.href = url;
        }
    }
};

console.log('Server.js carregado com sucesso!');
