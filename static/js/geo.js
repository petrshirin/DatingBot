function getGeoPosition() {
    navigator.geolocation.getCurrentPosition(position => {
        if (!window.location.href.includes('/profile/geo'))
            sendGeoPosition(position.coords)
        },
        error => {
            if (!window.location.href.includes('/profile/geo'))
                window.location.href = "/profile/geo/" + restaurant_id
        })
}

function sendGeoPosition(cords) {

    let body = {
        latitude: cords.latitude,
        longitude: cords.longitude
    }
    let request = new XMLHttpRequest()
    request.responseType = 'json'
    let restaurant_id = localStorage.getItem('restaurant_id')
    request.open('POST', "/api/check_geo/" + restaurant_id);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    request.addEventListener("readystatechange", () => {

        if (request.readyState === 4 && request.status === 200) {
            if (!request.response.status) {
                window.location.href = "/profile/geo/" + restaurant_id
            }

        }

    });
    request.send(JSON.stringify(body))
}

setTimeout(getGeoPosition(), 2000)









