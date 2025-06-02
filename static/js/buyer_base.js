document.addEventListener('DOMContentLoaded', function () {
    // Hamburger dropdown
    document.getElementById('hamburger')?.addEventListener('click', function(e) {
        e.stopPropagation();
        document.getElementById('dropdown')?.classList.toggle('show');
    });

    // Close dropdown when clicking anywhere else
    document.addEventListener('click', function(e) {
        const dropdown = document.getElementById('dropdown');
        const hamburger = document.getElementById('hamburger');
        if (!hamburger?.contains(e.target) && !dropdown?.contains(e.target)) {
            dropdown?.classList.remove('show');
        }
    });

    // See more genres
    document.getElementById('see-more')?.addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('more-genres')?.classList.toggle('show');
    });

    // Genre toggle
    document.getElementById('genre-toggle')?.addEventListener('click', function(e) {
        e.preventDefault();
        const panel = document.getElementById('genre-panel');
        panel?.classList.toggle('show-genre');
        const arrow = this.querySelector('i');
        if (arrow?.classList.contains('fa-chevron-right')) {
            arrow.classList.replace('fa-chevron-right', 'fa-chevron-down');
        } else {
            arrow?.classList.replace('fa-chevron-down', 'fa-chevron-right');
        }
    });

    // Close genre panel when clicking outside
    document.addEventListener('click', function(e) {
        const genrePanel = document.getElementById('genre-panel');
        const genreToggle = document.getElementById('genre-toggle');
        if (!genreToggle?.contains(e.target) && !genrePanel?.contains(e.target)) {
            genrePanel?.classList.remove('show-genre');
            const arrow = genreToggle?.querySelector('i');
            arrow?.classList.remove('fa-chevron-down');
            arrow?.classList.add('fa-chevron-right');
        }
    });

    // Genre box toggle
    const genreBrowse = document.querySelector('.genre-browse');
    const genreBox = document.getElementById('genre-box');

    genreBrowse?.addEventListener('click', function(e) {
        e.stopPropagation();
        genreBox?.classList.toggle('show-genre-box');
    });

    document.addEventListener('click', function(e) {
        if (!genreBox?.contains(e.target) && !genreBrowse?.contains(e.target)) {
            genreBox?.classList.remove('show-genre-box');
        }
    });
});
