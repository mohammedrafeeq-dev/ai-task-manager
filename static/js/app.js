document.addEventListener('DOMContentLoaded', function() {
    htmx.on('htmx:afterSettle', function(evt) {
        var el = document.getElementById('chat-messages');
        if (el) el.scrollTop = el.scrollHeight;
    });
});
