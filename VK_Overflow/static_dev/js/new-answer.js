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
            throw new Error(data.error || 'Network response was not ok.');
        });
    })
    .then(data => {
        if (data.html) {
            const container = document.getElementById('answers-container');
            container.insertAdjacentHTML('beforeend', data.html);

            document.getElementById('answer-text').value = '';

            const newAnswer = document.getElementById('answer-' + data.id);
            if (newAnswer) {
                newAnswer.scrollIntoView({ behavior: 'smooth' });
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorDiv.textContent = 'Произошла ошибка при отправке ответа.';
        errorDiv.style.display = 'block';
    });
});
