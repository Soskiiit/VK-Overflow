function debounce(func, delay) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), delay);
    };
}

const searchInput = document.querySelector('input[name="q"]');
searchInput.parentNode.style.position = 'relative';

// Results container (absolutely positioned inside the form wrapper)
let resultsContainer = document.createElement('div');
resultsContainer.className = 'dropdown-menu search-container';
resultsContainer.style.display = 'none';
searchInput.parentNode.appendChild(resultsContainer);

// Dimming overlay that covers the rest of the page while results are visible
let overlay = document.createElement('div');
overlay.className = 'search-overlay';
overlay.style.display = 'none';
document.body.appendChild(overlay);

const fetchResults = async (query) => {
    if (query.length < 3) {
        hideResults();
        return;
    }

    try {
        const response = await fetch(`/search-suggestions/?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        resultsContainer.innerHTML = '';
        console.log(data.results);
        if (data.results.length > 0) {
            data.results.forEach((item, index) => {
                const link = document.createElement('a');
                link.className = 'dropdown-item search-result';
                link.href = item.url;
                link.innerHTML = `<strong>${item.title}</strong> <small class="text-muted">(${item.likes} голосов)</small>`;
                
                // Animation
                link.style.opacity = '0';
                link.style.animation = `slideInFade 0.3s ease forwards`;
                link.style.animationDelay = `${index * 0.05}s`;
                
                resultsContainer.appendChild(link);
            });
            // Show results and overlay
            resultsContainer.style.display = 'block';
            overlay.style.display = 'block';
            // Allow CSS transition to run via adding the show class
            requestAnimationFrame(() => overlay.classList.add('show'));
        } else {
            resultsContainer.innerHTML = '<span class="dropdown-item search-result">Ничего не найдено</span>';
            resultsContainer.style.display = 'block';
            overlay.style.display = 'block';
            requestAnimationFrame(() => overlay.classList.add('show'));
        }
    } catch (error) {
        console.error('Ошибка поиска:', error);
    }
};

searchInput.addEventListener('input', debounce((e) => {
    fetchResults(e.target.value);
}, 300));

// Hide results and overlay helper
function hideResults() {
    resultsContainer.style.display = 'none';
    // hide overlay with transition
    overlay.classList.remove('show');
    // wait for transition then set display none
    setTimeout(() => {
        overlay.style.display = 'none';
    }, 200);
}

// Click outside: if click target not inside input or results, hide
document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
        hideResults();
    }
});

// Click on overlay should hide results
overlay.addEventListener('click', (e) => {
    hideResults();
});

// Close on Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        hideResults();
    }
});

// end of file