"use strict"

function upload() {
    const inpFile = document.getElementById("inpFile");
    const previewContainer = document.getElementById("imagePreview");
    const previewImage = previewContainer.querySelector(".imagePreviewImage");

    inpFile.addEventListener("change", function() {
        const file = this.files[0];

        if (file) {
            for (let i = 0; i < 2; i++) {
                document.getElementsByClassName("btn")[i].style.display = "block";
            }

            const reader = new FileReader();

            previewImage.style.display = "block";

            reader.addEventListener("load", function() {
                previewImage.setAttribute("src", this.result);
            })

            reader.readAsDataURL(file);

            document.querySelector(".photo").style.border = "none";
            document.getElementById("inpFile").style.display = "none";
        }
    })
}