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

let resultsContainer = document.createElement('div');
resultsContainer.className = 'dropdown-menu search-container show';
searchInput.parentNode.appendChild(resultsContainer);

const fetchResults = async (query) => {
    if (query.length < 3) {
        resultsContainer.style.display = 'none';
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
            resultsContainer.style.display = 'block';
        } else {
            resultsContainer.innerHTML = '<span class="dropdown-item search-result">Ничего не найдено</span>';
            resultsContainer.style.display = 'block';
        }
    } catch (error) {
        console.error('Ошибка поиска:', error);
    }
};

searchInput.addEventListener('input', debounce((e) => {
    fetchResults(e.target.value);
}, 300));

document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
        resultsContainer.style.display = 'none';
    }
});