document.addEventListener("DOMContentLoaded", function() {
    // 1. Dashboard Time Formatter (Fixes 4:30 AM/PM Glitch)
    document.querySelectorAll('.time-convert').forEach(el => {
        let timeString = el.innerText.trim();
        if (timeString && timeString.includes(':')) {
            let parts = timeString.split(':');
            let hours = parseInt(parts[0]);
            let minutes = parts[1].substring(0, 2);
            
            let ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12 || 12;
            
            el.innerText = `${hours}:${minutes} ${ampm}`;
        }
    });

    // 2. Chat Auto-Scroll to Bottom
    const chatBox = document.getElementById('chat-box');
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});

/**
 * UI Controls
 */
function toggleReschedule(dayId) {
    const form = document.getElementById(`reschedule-form-${dayId}`);
    if (form) form.classList.toggle('d-none');
}

function addResource() {
    alert('Resource upload coming soon! For the demo, use the chat to share links.');
}