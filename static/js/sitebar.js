window.onload = function () {
    var page = document.querySelector('.sitebar');
    page.onclick = menuShow;
    page.onmouseout = menuHide;

    function menuShow() {
        document.querySelector('#dark').style.display = 'block';
        var menu = document.querySelector('#menu');
        menu.style.top = 0;
        menu.style.left = 0;

    }
    function menuHide() {
        document.querySelector('#dark').style.display = 'none';
        document.querySelector('#menu').style.left = '-70%';
    }
}