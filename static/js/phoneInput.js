window.addEventListener("DOMContentLoaded", function() {
    function setCursorPosition(pos, elem) {
        elem.focus();
        if (elem.setSelectionRange) elem.setSelectionRange(pos, pos);
        else if (elem.createTextRange) {
            let range = elem.createTextRange();
            range.collapse(true);
            range.moveEnd("character", pos);
            range.moveStart("character", pos);
            range.select()
        }

        if (document.querySelector("#tel").value.length == 17) {
            document.getElementById("button").removeAttribute("disabled");
            document.querySelector(".btn").style.backgroundColor = "#F9D671";
        }
    }
    
    function mask(event) {
        let matrix = "+7(___) ___-__-__",
            i = 0,
            def = matrix.replace(/\D/g, ""),
            val = this.value.replace(/\D/g, "");
        if (def.length >= val.length) val = def;
        this.value = matrix.replace(/./g, function(a) {
            return /[_\d]/.test(a) && i < val.length ? val.charAt(i++) : i >= val.length ? "" : a
        });
        if (event.type == "blur") {
            if (this.value.length == 2) this.value = ""
        } else setCursorPosition(this.value.length, this)
    };
        let input = document.querySelector("#tel");
        input.addEventListener("input", mask, false);
        input.addEventListener("focus", mask, false);
        input.addEventListener("blur", mask, false);
    });

    
document.onkeydown = function(e) {
    if (e.keyCode == 8) {
        document.querySelector(".btn").style.backgroundColor = "#CFCDC8";  
    }
}

function getRestId() {
    splitUrl = window.location.href.split('/')
    return splitUrl[splitUrl.length-1]
}

localStorage.setItem('restaurant_id', getRestId())