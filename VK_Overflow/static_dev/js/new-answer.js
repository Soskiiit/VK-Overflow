document.getElementById('answer-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const text = document.getElementById('answer-text').value.trim();
    const errorDiv = document.getElementById('answer-error');

    if (text.length < 6) {
        errorDiv.textContent = 'Ответ должен быть не короче 6 символов';
        errorDiv.style.display = 'block';
        return;
    } else {
        errorDiv.style.display = 'none';
    }

    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return response.json().then(data => {
            if (data.error) {
                throw data.error;
            }
            throw new Error('Network response was not ok.');
        });
    })
    .then(data => {
        if (data.status === 'ok') {
            document.getElementById('answer-text').value = '';
            errorDiv.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        let errorMessage = 'Произошла ошибка при отправке ответа.';
        
        if (typeof error === 'object' && error !== null && !(error instanceof Error)) {
            errorMessage = Object.values(error).join('\n');
        } else if (error instanceof Error) {
            errorMessage = error.message;
        } else if (typeof error === 'string') {
            errorMessage = error;
        }
        
        errorDiv.textContent = errorMessage;
        errorDiv.style.display = 'block';
    });
});
