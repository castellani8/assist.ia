document.addEventListener('DOMContentLoaded', () => {
    const questionForm = document.getElementById('question-form');
    const questionInput = document.getElementById('question');
    const chatContainer = document.getElementById('chat-container');
    const submitBtn = document.getElementById('submit-btn');
    const loadingSpinner = document.getElementById('loading-spinner');
    const submitText = document.getElementById('submit-text');

    // Get token from localStorage or prompt user
    let token = localStorage.getItem('assist_ia_token');
    if (!token) {
        token = prompt('Please enter your API token:');
        if (token) {
            localStorage.setItem('assist_ia_token', token);
        }
    }

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');
        messageDiv.textContent = content;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function setLoading(isLoading) {
        if (isLoading) {
            loadingSpinner.classList.remove('d-none');
            submitText.textContent = 'Sending...';
            submitBtn.disabled = true;
        } else {
            loadingSpinner.classList.add('d-none');
            submitText.textContent = 'Send';
            submitBtn.disabled = false;
        }
    }

    questionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const question = questionInput.value.trim();
        if (!question) return;

        // Add user message to chat
        addMessage(question, true);
        questionInput.value = '';
        setLoading(true);

        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Token': token
                },
                body: JSON.stringify({
                    question: question
                })
            });

            if (response.status === 401) {
                // Token is invalid or missing
                localStorage.removeItem('assist_ia_token');
                token = prompt('Your token is invalid. Please enter a new token:');
                if (token) {
                    localStorage.setItem('assist_ia_token', token);
                    // Retry the request
                    questionForm.dispatchEvent(new Event('submit'));
                }
                return;
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request. Please try again.');
        } finally {
            setLoading(false);
        }
    });
}); 