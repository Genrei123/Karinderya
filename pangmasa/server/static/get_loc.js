document.addEventListener('DOMContentLoaded', function () {
    let button = document.getElementById('get_location')

    button.addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                let longitude = document.getElementById('longitude');
                let latitude = document.getElementById('latitude');

                longitude.value = `${position.coords.latitude}`;
                latitude.value = `${position.coords.longitude}`;
            });
        }
    });








});


