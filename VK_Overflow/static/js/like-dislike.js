function updateRatingBlock(rating_block, json) {
    let arrow_up = rating_block.children[0];
    let counter = rating_block.children[1];
    let arrow_down = rating_block.children[2];
    switch (json.user_vote) {
        case 0:
            if (arrow_down.classList.contains('rating-down-clicked')) {
                counter.textContent = String(Number(counter.textContent) + 1);
            } else {
                counter.textContent = String(Number(counter.textContent) - 1);
            }
            arrow_up.classList.remove('rating-up-clicked');
            arrow_down.classList.remove('rating-down-clicked');
            break;
        case 1:
            if (arrow_down.classList.contains('rating-down-clicked')) {
                counter.textContent = String(Number(counter.textContent) + 2);
            } else {
                counter.textContent = String(Number(counter.textContent) + 1);
            }
            arrow_up.classList.add('rating-up-clicked');
            arrow_down.classList.remove('rating-down-clicked');
            break;
        case -1:
            if (arrow_up.classList.contains('rating-up-clicked')) {
                counter.textContent = String(Number(counter.textContent) - 2);
            } else {
                counter.textContent = String(Number(counter.textContent) - 1);
            }
            arrow_up.classList.remove('rating-up-clicked');
            arrow_down.classList.add('rating-down-clicked');
            break;
    }
}

function voteQuestion(question_id, action) {
    fetch('/vote/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({
            question_id: question_id,
            action: action,
        }
        )}).then(response => response.json()).then(json => {
            let rating_block = document.getElementById(`rating-block-${question_id}`);
            updateRatingBlock(rating_block, json);
    })
}

function voteAnswer(answer_id, action) {
    fetch('/vote/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({
            answer_id: answer_id,
            action: action,
        }
        )}).then(response => response.json()).then(json => {
            let rating_block = document.getElementById(`ans-rating-block-${answer_id}`);
            updateRatingBlock(rating_block, json);
    })
}

function markBestAnswer(questionId, answerId, authorId) {
    fetch('/set-best-answer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({
            question_id: questionId,
            answer_id: answerId,
            author: authorId
        })
    }).then(response => response.json()).then(json => {
        if (json.status === 'ok') {
            document.querySelectorAll('.best-answer-icon').forEach(icon => {
                icon.classList.remove('text-success');
                icon.classList.add('text-secondary');
            });

            const clickedIcon = document.getElementById(`best-answer-icon-${answerId}`);
            if (clickedIcon) {
                clickedIcon.classList.remove('text-secondary');
                clickedIcon.classList.add('text-success');
            }
        } else {
            console.error(json.error);
        }
    });
}
