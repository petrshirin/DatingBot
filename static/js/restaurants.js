function change_rest(rest_id) {
    let request = new XMLHttpRequest();
    request.responseType = 'json';
    request.open('GET', "/api/change_rest/" + rest_id);
    request.addEventListener("readystatechange", () => {

    if (request.readyState === 4 && request.status === 200) {
        document.getElementById("choice1").checked=false;
        document.getElementById("choice2").checked=false;
        document.getElementById("choice3").checked=false;
        document.getElementById("choice"+rest_id).checked=true;
        console.log(request.response);
    }
    });
    request.send();
}