function get_user() {
    let request = new XMLHttpRequest();
    request.responseType = 'json';
    request.open('GET', "/api/get_user/");
    request.addEventListener("readystatechange", () => {

    if (request.readyState === 4 && request.status === 200) {
        user = request.response;
        if (user['error'] == 'Not users') {
            window.location.href = '/profile/notusers/';
            current_user = null;
            return;
        }
        current_user = user

        document.getElementById('userName').innerHTML = user['first_name'] + ", " + (user['age'] ? user['age'] : "");
        document.getElementById('userStatus').innerHTML = user['status'] ? user['status'] : "";
        if (user.photo) {
            document.getElementById('userPhoto').src = user.photo;
        }
        else {
            document.getElementById('userPhoto').src = null;
        }
    }
    });
    request.send();
}


function like_user() {
    let request = new XMLHttpRequest();
    request.responseType = 'json';

    if (current_user) {
        request.open('GET', "/api/like_user/"+ current_user.pk + "/");
        request.addEventListener("readystatechange", () => {

        if (request.readyState === 4 && request.status === 200) {
            get_user()
        }
        });
        request.send();
    }
}


function dislike_user() {
    let request = new XMLHttpRequest();
    request.responseType = 'json';

    if (current_user) {
        request.open('GET', "/api/dislike_user/"+ current_user.pk + "/");
        request.addEventListener("readystatechange", () => {

        if (request.readyState === 4 && request.status === 200) {
            get_user()
        }
        });
        request.send();
    }
}

get_user()
