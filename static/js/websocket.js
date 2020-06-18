
var website = window.location.host;

try{
    var sock = new WebSocket('ws://' + website + '/ws');
}
catch(err){
    var sock = new WebSocket('wss://' + website + '/ws');
}




// show message in div#subscribe
function showMessage(message) {
    lastMsg( orientation(0) );

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

    lastMsg( orientation(1) );
    document.querySelector(".messages > div:last-child").scrollIntoView();
}


sock.onopen = function(){

    let request = new XMLHttpRequest();
    request.responseType = 'json';
    request.open('GET', "/api/chat_info/");
    request.addEventListener("readystatechange", () => {

    if (request.readyState === 4 && request.status === 200) {
        data = request.response
        let s_msg = {
        "text": '|open|',
        "chat_id": data.user_id,
        "token": data.token
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
        return;
    }
    showMessage(data);
};


sock.onclose = function(event){
    if(event.wasClean){
        showMessage({
        'text': 'Clean connection end',
        'chat_id': 0
        });
    }
    else{
        showMessage({
        'text': 'Connection broken',
        'chat_id': 0
        });
    }
};

sock.onerror = function(error){
    showMessage({
        'text': error,
        'chat_id': 0
        });
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
    if (!(min / 10)) min = '0' + min;
    if (!(hours / 10)) hours = '0' + hours;
    time = hours + ':' + min;
    return time;
}


function sendMessage() {
    lastMsg( orientation(0) );

    let msg = document.querySelector("#textInp").value;
    split_url = window.location.href.split('/');
    let s_msg = {
        "text": msg,
        "chat_id": Number(split_url[split_url.length - 1])
    };
    console.log(s_msg)
    sock.send(JSON.stringify(s_msg));
    addMyMsg(msg);
    document.querySelector("#textInp").value = "";

    lastMsg( orientation(1) );
    document.querySelector(".messages > div:last-child").scrollIntoView();
}

function lastMsg(bottom) {
    document.querySelector(".messages > div:last-child").style.marrginBottom = bottom;
}

function orientation(mode) { // mode - новое (1) или старое (0) последнее сообщение
    let orientation = screen.orientation.type;
    if (mode) return orientation.includes("portrait") ? "360px" : "180px";
    else return orientation.includes("portrait") ? "120px" : "60px";
}





//document.querySelector('.inpField > input').addEventListener("click", sendMessage() )