document.addEventListener('DOMContentLoaded', () => {
    // Chatbot Toggle
    const chatbotBtn = document.getElementById('chatbot-toggle');
    const chatbotWindow = document.getElementById('chatbot-window');
    const closeChat = document.getElementById('close-chat');

    if (chatbotBtn && chatbotWindow) {
        chatbotBtn.addEventListener('click', () => {
            chatbotWindow.classList.toggle('open');
            // focus input if opening
            if(chatbotWindow.classList.contains('open')) {
                document.getElementById('chat-input-text').focus();
            }
        });
    }

    if (closeChat) {
        closeChat.addEventListener('click', () => {
            chatbotWindow.classList.remove('open');
        });
    }

    // Chatbot Send Message
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input-text');
    const chatBody = document.getElementById('chat-body');

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const msg = chatInput.value.trim();
            if (!msg) return;

            // Add User message
            appendMessage(msg, 'user');
            chatInput.value = '';

            // Show loading placeholder
            const typingIndicator = appendMessage('Typing...', 'bot', true);

            try {
                // Send to backend
                const response = await fetch('/chatbot_api', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg })
                });
                
                const data = await response.json();
                
                // Remove indicator and show reply
                typingIndicator.remove();
                appendMessage(data.reply, 'bot');

            } catch (err) {
                console.error('Chat API Error:', err);
                typingIndicator.remove();
                appendMessage("Sorry, I'm having trouble connecting right now.", 'bot');
            }
        });
    }

    function appendMessage(text, sender, isTyping = false) {
        const div = document.createElement('div');
        div.className = `chat-msg msg-${sender}`;
        div.textContent = text;
        if(isTyping) div.style.opacity = '0.5';
        
        chatBody.appendChild(div);
        
        // auto-scroll
        chatBody.scrollTop = chatBody.scrollHeight;
        return div;
    }
});
