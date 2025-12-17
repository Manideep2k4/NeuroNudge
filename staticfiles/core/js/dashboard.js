document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('habitCalendar');
    const dataElement = document.getElementById('habit-events-data');

    if (calendarEl && dataElement) {
        const eventsData = JSON.parse(dataElement.textContent);

        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            height: 'auto',
            events: eventsData
        });

        calendar.render();
    }

    // Pomodoro Countdown
    const startInput = document.getElementById("pomodoro-start");
    const countdown = document.getElementById("countdown");

    if (startInput && countdown) {
        const startTime = new Date(startInput.value);
        const endTime = new Date(startTime.getTime() + 25 * 60000);

        function updateCountdown() {
            const now = new Date();
            const remaining = endTime - now;

            if (remaining <= 0) {
                countdown.textContent = "⏰ Time's up!";
                return;
            }

            const mins = Math.floor(remaining / 60000);
            const secs = Math.floor((remaining % 60000) / 1000);
            countdown.textContent = `🕒 Time Left: ${mins}m ${secs < 10 ? '0' : ''}${secs}s`;

            setTimeout(updateCountdown, 1000);
        }

        updateCountdown();
    }
});
