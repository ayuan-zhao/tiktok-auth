$(document).ready(function () {
    $('#login-btn').click(function () {
        // Send a GET request to our Flask backend
        $.get('/login-tiktok', function (data) {
            // If the backend returns a URL, redirect the user to that URL
            if (data.url) {
                window.location.href = data.url;
                $('#logout-btn').show();
                $('#login-btn').hide();
            }
        });
    });

    $('#logout-btn').click(function () {
        // Send a GET request to our Flask backend for logout
        $.get('/logout', function () {
            // Once logged out, hide the logout button and show the login button
            $('#logout-btn').hide();
            $('#login-btn').show();
        });
    });
});
