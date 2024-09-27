function toggleMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    mobileMenu.style.display = (mobileMenu.style.display === 'flex') ? 'none' : 'flex';
}

// Закрытие меню при нажатии вне его
window.onclick = function(event) {
    const mobileMenu = document.getElementById('mobileMenu');
    if (!event.target.matches('.hamburger') && !mobileMenu.contains(event.target)) {
        mobileMenu.style.display = 'none';
    }
}

// Убедимся, что мобильное меню скрыто при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
    const mobileMenu = document.getElementById('mobileMenu');
    mobileMenu.style.display = 'none'; // Скрываем мобильное меню на загрузке страницы
});