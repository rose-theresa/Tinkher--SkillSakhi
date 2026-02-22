// Simple View Routing Logic for Hackathon Demo
document.addEventListener('DOMContentLoaded', () => {
    // Navigation elements
    const navHome = document.getElementById('nav-home');
    const navDashboard = document.getElementById('nav-dashboard');
    const btnGetStarted = document.getElementById('btn-get-started');
    const logo = document.getElementById('logo');

    // View elements
    const viewHome = document.getElementById('view-home');
    const viewDashboard = document.getElementById('view-dashboard');

    // Setup Current Date in Dashboard
    const dateDisplay = document.getElementById('current-date');
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    dateDisplay.textContent = new Date().toLocaleDateString('en-US', options);

    // Event Listeners for Navigation
    navHome.addEventListener('click', (e) => {
        e.preventDefault();
        switchToHome();
    });

    logo.addEventListener('click', (e) => {
        e.preventDefault();
        switchToHome();
    });

    navDashboard.addEventListener('click', (e) => {
        e.preventDefault();
        switchToDashboard();
    });

    btnGetStarted.addEventListener('click', (e) => {
        e.preventDefault();
        switchToDashboard();
    });

    // Make switching available globally
    window.switchToDashboard = switchToDashboard;
    window.switchToHome = switchToHome;
});

function switchToHome() {
    // Update nav active state
    document.getElementById('nav-home').classList.add('active');
    document.getElementById('nav-dashboard').classList.remove('active');

    // Update views
    document.getElementById('view-dashboard').classList.remove('active-view');
    document.getElementById('view-home').classList.add('active-view');
    window.scrollTo(0, 0);
}

function switchToDashboard() {
    // Update nav active state
    document.getElementById('nav-dashboard').classList.add('active');
    document.getElementById('nav-home').classList.remove('active');

    // Update views
    document.getElementById('view-home').classList.remove('active-view');
    document.getElementById('view-dashboard').classList.add('active-view');
    window.scrollTo(0, 0);
}

// Tab Switching in Dashboard
function switchTab(tabId) {
    // Reset buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Set clicked button active
    event.target.classList.add('active');

    // Hide all contents
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));

    // Show target content
    document.getElementById(`tab-${tabId}`).classList.add('active');
}
