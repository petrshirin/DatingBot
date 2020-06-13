function checkTxt() {
    if (document.getElementById("me").value) {
        document.querySelector(".btn").style.backgroundColor = "#F9D671";
    }
}

document.onkeydown = function(e) {
    if (e.keyCode == 8 && document.getElementById("me").value.length == 0 ) {
        document.querySelector(".btn").style.backgroundColor = "#CFCDC8";
    }  
}; 