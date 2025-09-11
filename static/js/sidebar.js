document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    const toggleBtn = document.getElementById('toggleSidebar');
    const closeBtn = document.getElementById('closeSidebar');
    let overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    function toggleSidebar() {
        sidebar.classList.toggle('show');
        mainContent.classList.toggle('sidebar-expanded');
        overlay.classList.toggle('show');
    }

    function closeSidebar() {
        sidebar.classList.remove('show');
        mainContent.classList.remove('sidebar-expanded');
        overlay.classList.remove('show');
    }

    // Toggle sidebar when menu button is clicked
    toggleBtn.addEventListener('click', toggleSidebar);

    // Close sidebar when close button is clicked
    closeBtn.addEventListener('click', closeSidebar);

    // Close sidebar when clicking outside
    overlay.addEventListener('click', closeSidebar);

    // Close sidebar on window resize if screen becomes too small
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 992 && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });

    // Close sidebar when pressing escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });
}); 