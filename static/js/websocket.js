
var website = window.location.host;
var sock = null;

function create_websocket() {
    try{
        sock = new WebSocket('ws://' + website + '/ws');
    }
    catch(err){
        sock = new WebSocket('wss://' + website + '/ws');
    }
}

create_websocket();

sock.onopen = function(){
    let request = new XMLHttpRequest();
    request.responseType = 'json';
    request.open('GET', "/api/chat_info/");
    request.addEventListener("readystatechange", () => {

    if (request.readyState === 4 && request.status === 200) {
        data = request.response
        splitUrl = window.location.href.split('/');
        let s_msg = {
        "text": '|open|',
        "chat_id": data.user_id,
        "token": data.token,
        "partner_id": Number(splitUrl[splitUrl.length - 1])
    };
    sock.send(JSON.stringify(s_msg));
    }
    });
    request.send();

}

// income message handler
sock.onmessage = function(event) {
    data = JSON.parse(event.data);
    if (data['text'] == '|open|') {
        console.log(data);
    }
    else {
        showMessage(data);
    }
};


sock.onclose = function(event){
    if(event.wasClean){
        showMessage({
        'text': 'Соединения окончено, если это сделани не вы, перезагрузите страницу',
        'chat_id': 0
        });
    }
    else{
        sock = null;
        setTimeout(create_websocket, 5000);
    }
};

sock.onerror = function(error){
    showMessage({
        'text': error,
        'chat_id': 0
        });
}



// show message in div#subscribe
function showMessage(message) {

    let messages = document.querySelector(".messages");

    if (message.chat_id == 0) {
        addMyMsg(message.text);
    }
    else {
        let div = document.createElement("div");

        // Как должно быть с картинкой
        // <div><img class="partnerPhoto" src="../svg/Rectangle 25.svg" /></div>

        let imgDiv = "<div><img class='partnerPhoto' src='" + sessionStorage.getItem("partnerPhoto") + "'/></div>"
        let timeDiv = "<div class='theirTime date'>" + getTime() + "</div>";
        let msgDiv = "<div class='theirs'>" + data.text + "</div>";

        div.innerHTML = imgDiv + msgDiv + timeDiv;
        // div.innerHTML = msgDiv + timeDiv;
        div.className = "partner";

        messages.append(div);
    };

}

function addMyMsg(msg) {
    let messages = document.querySelector(".messages");

    let div = document.createElement("div");

    let timeDiv = "<div class='myTime date'>" + getTime() + "</div>";
    let msgDiv = "<div class='mine'>" + msg + "</div>";

    div.innerHTML = timeDiv + msgDiv;
    div.className = "me";

    messages.append(div);
}

function getTime() {
    let time = new Date();
    let min = time.getMinutes();
    let hours = time.getHours();
    if (!Math.trunc(min / 10)) min = '0' + min;
    if (!Math.trunc(hours / 10)) hours = '0' + hours;
    time = hours + ':' + min;
    return time;
}


function sendMessage() {

    let msg = document.querySelector("#textInp").value;
    if (msg) {
        document.querySelector("#textInp").value = "";
        splitUrl = window.location.href.split('/');
        let sMsg = {
            "text": msg,
            "chat_id": Number(splitUrl[splitUrl.length - 1])
        };
        sock.send(JSON.stringify(sMsg));
        addMyMsg(msg);

        document.querySelector("#send").style.backgroundColor = "#343434";

        let inp = document.getElementById("textInp");
        let primary = "";
        let orientation = window.screen.orientation.type;
        if (orientation.includes("landscape")) {
            primary = "44px";
        } else {
            primary = "75px";
        }
        if (inp.style.height !== primary) {
            inp.style.height = primary;
        }
    scrollToLastMsg();
    }

}

function deleteLastMessage() {
     let messages_block = document.querySelector(".messages");
     messages = messages_block.getElementsByClassName('me')
     messages[messages.length - 1].remove()
}

function scrollToLastMsg() {
    block = document.querySelector('html');
    block.scrollTop = block.scrollHeight;
}



scrollToLastMsg();