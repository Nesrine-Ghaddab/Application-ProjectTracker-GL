// Enhanced Chatbot Widget with Modern Design
document.addEventListener('DOMContentLoaded', function() {
    // Create chatbot button with animation
    const chatbotButton = document.createElement('div');
    chatbotButton.id = 'chatbot-button';
    chatbotButton.innerHTML = '💬';
    chatbotButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 24px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        z-index: 1000;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    `;
    chatbotButton.onmouseover = () => chatbotButton.style.transform = 'scale(1.1)';
    chatbotButton.onmouseout = () => chatbotButton.style.transform = 'scale(1)';
    document.body.appendChild(chatbotButton);

    // Create chat window with modern design
    const chatWindow = document.createElement('div');
    chatWindow.id = 'chatbot-window';
    chatWindow.style.cssText = `
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 350px;
        height: 500px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border: none;
        border-radius: 20px;
        display: none;
        flex-direction: column;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 1000;
        overflow: hidden;
        transform: scale(0);
        transition: transform 0.3s ease;
    `;
    chatWindow.innerHTML = `
        <div id="chatbot-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 20px 20px 0 0; cursor: move; display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: bold; font-size: 16px;">Work Assistant</div>
            <span id="chatbot-close" style="cursor: pointer; font-size: 20px; transition: transform 0.2s;">×</span>
        </div>
        <div id="chatbot-messages" style="flex: 1; padding: 15px; overflow-y: auto; height: 350px; background: rgba(255,255,255,0.8);"></div>
        <div id="typing-indicator" style="display: none; padding: 10px; color: #666; font-style: italic;">Assistant is typing...</div>
        <div id="quick-buttons" style="padding: 10px; display: flex; gap: 5px; flex-wrap: wrap; background: rgba(255,255,255,0.9);">
            <button class="quick-btn" data-message="Show my projects">Projects</button>
            <button class="quick-btn" data-message="What tasks do I have?">Tasks</button>
            <button class="quick-btn" data-message="Upcoming meetings">Meetings</button>
            <button class="quick-btn" data-message="My notes">Notes</button>
        </div>
        <div id="chatbot-input" style="padding: 15px; border-top: 1px solid rgba(0,0,0,0.1); background: white;">
            <div style="display: flex; gap: 10px;">
                <input type="text" id="chatbot-input-field" placeholder="Ask about your work..." style="flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 20px; outline: none; transition: border-color 0.3s;">
                <button id="chatbot-send" style="padding: 10px 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 20px; cursor: pointer; transition: transform 0.2s;">Send</button>
            </div>
        </div>
    `;
    document.body.appendChild(chatWindow);

    // Add styles for quick buttons
    const style = document.createElement('style');
    style.textContent = `
        .quick-btn {
            padding: 5px 10px;
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
        }
        .quick-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        @keyframes pulse {
            0% { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
            50% { box-shadow: 0 4px 20px rgba(102, 126, 234, 0.6); }
            100% { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
        }
        .message-bubble {
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 18px;
            margin: 5px 0;
            word-wrap: break-word;
            animation: fadeIn 0.3s ease;
        }
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background: white;
            color: #333;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);

    // Toggle chat window with animation
    chatbotButton.addEventListener('click', function() {
        if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
            chatWindow.style.display = 'flex';
            setTimeout(() => chatWindow.style.transform = 'scale(1)', 10);
        } else {
            chatWindow.style.transform = 'scale(0)';
            setTimeout(() => chatWindow.style.display = 'none', 300);
        }
    });

    // Close chat
    document.getElementById('chatbot-close').addEventListener('click', function() {
        chatWindow.style.transform = 'scale(0)';
        setTimeout(() => chatWindow.style.display = 'none', 300);
    });

    // Quick buttons functionality
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const message = this.getAttribute('data-message');
            document.getElementById('chatbot-input-field').value = message;
            sendMessage();
        });
    });

    // Send message with enhanced UI
    function sendMessage() {
        const inputField = document.getElementById('chatbot-input-field');
        const message = inputField.value.trim();
        if (!message) return;

        // Add user message with bubble
        const messagesDiv = document.getElementById('chatbot-messages');
        const userBubble = document.createElement('div');
        userBubble.className = 'message-bubble user-message';
        userBubble.textContent = message;
        messagesDiv.appendChild(userBubble);
        inputField.value = '';

        // Show typing indicator
        const typingIndicator = document.getElementById('typing-indicator');
        typingIndicator.style.display = 'block';
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // Send to server
        fetch('/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.style.display = 'none';
            if (data.response) {
                const botBubble = document.createElement('div');
                botBubble.className = 'message-bubble bot-message';
                botBubble.innerHTML = `<strong>Assistant:</strong> ${data.response}`;
                messagesDiv.appendChild(botBubble);
            } else {
                const errorBubble = document.createElement('div');
                errorBubble.className = 'message-bubble bot-message';
                errorBubble.innerHTML = `<strong>Error:</strong> ${data.error}`;
                errorBubble.style.color = '#e74c3c';
                messagesDiv.appendChild(errorBubble);
            }
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        })
        .catch(error => {
            typingIndicator.style.display = 'none';
            const errorBubble = document.createElement('div');
            errorBubble.className = 'message-bubble bot-message';
            errorBubble.innerHTML = `<strong>Error:</strong> Unable to connect`;
            errorBubble.style.color = '#e74c3c';
            messagesDiv.appendChild(errorBubble);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        });
    }

    document.getElementById('chatbot-send').addEventListener('click', sendMessage);
    document.getElementById('chatbot-input-field').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});