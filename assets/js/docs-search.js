(function() {
  'use strict';

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSearch);
  } else {
    initSearch();
  }

  function initSearch() {
    const searchInput = document.getElementById('docs-search');
    const resultsContainer = document.getElementById('search-results');

    if (!searchInput || !resultsContainer) return;

    let searchIndex = null;
    let documents = [];
    let debounceTimer = null;

    // Load search index
    fetch('/en/docs/index.json')
      .then(response => response.json())
      .then(data => {
        documents = data;

        // Build Lunr index
        searchIndex = lunr(function() {
          this.ref('id');
          this.field('title', { boost: 10 });
          this.field('description', { boost: 5 });
          this.field('content');

          documents.forEach(doc => {
            this.add(doc);
          });
        });

        console.log('Search index loaded with', documents.length, 'documents');
      })
      .catch(err => {
        console.error('Failed to load search index:', err);
      });

    // Handle search input
    searchInput.addEventListener('input', function(e) {
      const query = e.target.value.trim();

      clearTimeout(debounceTimer);

      if (query.length < 2) {
        hideResults();
        return;
      }

      debounceTimer = setTimeout(() => {
        performSearch(query);
      }, 300);
    });

    // Handle keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
      const items = resultsContainer.querySelectorAll('.search-result-item');
      const currentFocus = resultsContainer.querySelector('.search-result-item.focused');
      let index = Array.from(items).indexOf(currentFocus);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        index = index < items.length - 1 ? index + 1 : 0;
        if (items[index]) {
          items.forEach(item => item.classList.remove('focused'));
          items[index].classList.add('focused');
          items[index].scrollIntoView({ block: 'nearest' });
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        index = index > 0 ? index - 1 : items.length - 1;
        if (items[index]) {
          items.forEach(item => item.classList.remove('focused'));
          items[index].classList.add('focused');
          items[index].scrollIntoView({ block: 'nearest' });
        }
      } else if (e.key === 'Enter' && currentFocus) {
        e.preventDefault();
        const link = currentFocus.querySelector('a');
        if (link) link.click();
      } else if (e.key === 'Escape') {
        hideResults();
        searchInput.blur();
      }
    });

    // Close results when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
        hideResults();
      }
    });

    function performSearch(query) {
      if (!searchIndex) {
        resultsContainer.innerHTML = '<div class="search-loading">Loading search index...</div>';
        resultsContainer.classList.add('visible');
        return;
      }

      try {
        // Perform fuzzy search
        const results = searchIndex.query(function(q) {
          // Exact match boost
          query.split(/\s+/).forEach(term => {
            q.term(term, { boost: 100 });
            q.term(term, {
              boost: 10,
              usePipeline: true,
              wildcard: lunr.Query.wildcard.TRAILING
            });
            q.term(term, {
              boost: 1,
              usePipeline: true,
              editDistance: 1
            });
          });
        });

        displayResults(results, query);
      } catch (err) {
        console.error('Search error:', err);
        resultsContainer.innerHTML = '<div class="search-no-results">Search error. Please try again.</div>';
        resultsContainer.classList.add('visible');
      }
    }

    function displayResults(results, query) {
      if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="search-no-results">No results found</div>';
        resultsContainer.classList.add('visible');
        return;
      }

      const maxResults = 10;
      const displayResults = results.slice(0, maxResults);

      let html = '<div class="search-results-list">';

      displayResults.forEach(result => {
        const doc = documents.find(d => d.id === result.ref);
        if (!doc) return;

        // Highlight matching terms
        const highlightedTitle = highlightMatches(doc.title, query);
        const highlightedDesc = highlightMatches(
          doc.description || truncateContent(doc.content, 150),
          query
        );

        html += `
          <div class="search-result-item">
            <a href="${doc.url}">
              <div class="search-result-title">${highlightedTitle}</div>
              <div class="search-result-description">${highlightedDesc}</div>
              <div class="search-result-url">${doc.url}</div>
            </a>
          </div>
        `;
      });

      if (results.length > maxResults) {
        html += `<div class="search-results-more">${results.length - maxResults} more results...</div>`;
      }

      html += '</div>';

      resultsContainer.innerHTML = html;
      resultsContainer.classList.add('visible');
    }

    function highlightMatches(text, query) {
      if (!text) return '';

      const terms = query.toLowerCase().split(/\s+/);
      let highlighted = text;

      terms.forEach(term => {
        const regex = new RegExp(`(${escapeRegex(term)})`, 'gi');
        highlighted = highlighted.replace(regex, '<mark>$1</mark>');
      });

      return highlighted;
    }

    function escapeRegex(string) {
      return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function truncateContent(content, maxLength) {
      if (!content || content.length <= maxLength) return content || '';
      return content.substring(0, maxLength).trim() + '...';
    }

    function hideResults() {
      resultsContainer.classList.remove('visible');
      resultsContainer.innerHTML = '';
    }
  }
})();
