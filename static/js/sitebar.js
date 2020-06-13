document.getElementById("getMenuBar").addEventListener("click", ()=> {
    document.querySelector("#menu").style.display = "block";

    document.getElementById("mainWindow").style.display = "none";
})

document.getElementById("close").addEventListener("click", ()=> {
    document.querySelector("#menu").style.display = "none";

    document.getElementById("mainWindow").style.display = "block";
})