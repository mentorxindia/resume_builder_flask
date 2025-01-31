
document.addEventListener('DOMContentLoaded', () => {
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        new bootstrap.Dropdown(dropdown);
    });

    // $('#sidebarCollapse').on('click', function () {
    //     $('#sidebar').toggleClass('active');
    //     $('#content').toggleClass('active');
    // });
});