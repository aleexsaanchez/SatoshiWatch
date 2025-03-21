document.addEventListener('DOMContentLoaded', () => {
    // Typing effect for welcome message
    const welcomeText = document.getElementById('welcome-text');
    const message = "Welcome to SatoshiWatch";
    let i = 0;

    function typeWriter() {
        if (i < message.length) {
            welcomeText.textContent += message.charAt(i);
            i++;
            setTimeout(typeWriter, 100);
        }
    }
    if (welcomeText) {
        typeWriter(); // Only run if welcomeText exists
    }

    // FAB toggle
    const fab = document.querySelector('.fab');
    const fabMenu = document.querySelector('.fab-menu');

    if (fab && fabMenu) {
        fab.addEventListener('click', () => {
            fabMenu.style.display = fabMenu.style.display === 'flex' ? 'none' : 'flex';
        });
    } else {
        console.error('FAB or FAB menu not found in the DOM');
    }

    // Button hover effect
    const buttons = document.querySelectorAll('.cta-button');
    buttons.forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.boxShadow = '0 0 20px #00d4ff';
        });
        button.addEventListener('mouseout', () => {
            button.style.boxShadow = 'none';
        });
    });
});