function checkEmptiness(element) {

    document.querySelector(".advice > div:last-child").style.display = "none";
    document.querySelector(".samples").style.display = "none";

    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
    if (element.value) {
        document.querySelector("#send").style.backgroundColor = "#F9D671";
    }
}

let inp = document.getElementById("textInp");


inp.addEventListener("focusout", ()=> {
    document.querySelector(".advice > div:last-child").style.display = "block";
    document.querySelector(".samples").style.display = "block";
    fixHeight();    
})

document.onkeydown = function(e) {
    if (e.keyCode == 8 && inp.value.length == 0 ) {
        document.querySelector("#send").style.backgroundColor = "#343434";
    }

    fixHeight();    
}; 

document.addEventListener("click", (event)=> {
    let target = event.target.innerHTML;

    let samples = document.getElementById("samples").children;

    for (let i = 0; i < samples.length; i++) {
        if (samples[i].innerHTML === target) {
            inp.value = target;
            if ( screen.orientation.type.includes("portrait") ) {
                document.querySelector("#textInp").style.height = "180px";
            } else {
                document.querySelector("#textInp").style.height = "90px";
            }
        }
    }
})

function fixHeight() {
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
