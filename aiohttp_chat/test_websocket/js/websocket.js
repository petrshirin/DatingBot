try{
    var sock = new WebSocket('ws://' + "127.0.0.1:8080" + '/ws');
}
catch(err){
    var sock = new WebSocket('wss://' + "127.0.0.1:8080" + '/ws');
}

// show message in div#subscribe
function showMessage(message) {
    document.getElementsByClassName('text')[0].innerHTML += message + '<br>';
}

function sendMessage(){
    let msg =  document.getElementById("inp")
    let s_msg = {
        "text": msg.value,
        "chat_id": 1
    };
    sock.send(JSON.stringify(s_msg));
    msg.value = '';
}

sock.onopen = function(){
    showMessage('Connection to server started')
    data {
        user_id: 1,
        token: "test_token"
    }

    let s_msg = {
        "text": '|open|',
        "chat_id": data.user_id,
        "token": data.token
    };
    sock.send(JSON.stringify(s_msg));
}

// income message handler
sock.onmessage = function(event) {
  showMessage(event.data);
};


sock.onclose = function(event){
    if(event.wasClean){
        showMessage('Clean connection end');
    }
    else{
        showMessage('Connection broken');
    }
};

sock.onerror = function(error){
    showMessage(error);
}