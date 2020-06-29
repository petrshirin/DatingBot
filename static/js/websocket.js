
var website = window.location.host;

try{
    var sock = new WebSocket('ws://' + website + '/ws');
}
catch(err){
    var sock = new WebSocket('wss://' + website + '/ws');
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
    deleteLastMessage();

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
    }

}




function deleteLastMessage() {
     let messages_block = document.querySelector(".messages");
     messages = messages_block.getElementsByClassName('me')
     messages[messages.length - 1].remove()
}

//document.getElementById('send').addEventListener('touchstart', function(e){
//        sendMessage();
//}, false);

//document.getElementById("send").ontouchstart = sendMessage;
// Если не сработает, можно попробовать в HTML у #send прописать ontouchstart="sendMessage(ent)"

//document.querySelector('.inpField > input').addEventListener("click", sendMessage() )
