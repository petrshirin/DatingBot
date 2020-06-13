function checkAge(key) {
    key = +key;
    if (isNaN(key) || 
        (key === 0 && document.getElementById("age").value.length == 0) ) {
        event.preventDefault();
    } else {
        document.querySelector(".btn").style.backgroundColor = "#F9D671";
    }
};

document.onkeydown = function(e) {
    if (!document.getElementById("age").value) {
        document.querySelector(".btn").style.backgroundColor = "#CFCDC8";
    }  
};