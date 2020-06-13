function checkNnT() {
    let radiobtn = document.getElementsByName("sex");
    if ( (radiobtn[0].checked || radiobtn[1].checked) && document.getElementById("myName").value ) {
        document.getElementById("button").removeAttribute("disabled");
        document.querySelector(".btn").style.backgroundColor = "#F9D671";
    }
};

document.onkeydown = function(e) {
    if (document.getElementById("myName").value) {
        document.querySelector(".btn").style.backgroundColor = "#CFCDC8";
    }  
}