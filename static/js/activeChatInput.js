function checkEmptiness(element) {

    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
    if (element.value) {
        document.querySelector("#send").style.backgroundColor = "#F9D671";
    }
    document.querySelector('.input').scrollTo(0, document.querySelector('.input').scrollHeight)
}

let inp = document.getElementById("textInp");

document.onkeydown = function(e) {
    if (e.keyCode == 8 && inp.value.length <= 1 ) {
        document.querySelector("#send").style.backgroundColor = "#343434";
    }

    fixHeight();    
}; 

function fixHeight() {
    let primary = "";
    let orientation = window.screen.orientation.type;
    if (orientation.includes("landscape")) {
        primary = "44px";
    } else {
        primary = "85px";
    }
    if (inp.style.height !== primary) {
        inp.style.height = primary;
    }
}

sessionStorage.setItem("partnerPhoto", document.getElementsByClassName('partnerPhoto_hidden')[0].src)