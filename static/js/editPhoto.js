"use strict"

function upload() {
    const inpFile = document.getElementById("inpFile");
    const previewContainer = document.getElementById("imagePreview");
    const previewImage = previewContainer.querySelector(".imagePreviewImage");

    inpFile.addEventListener("change", function() {
        const file = this.files[0];

        console.log(file);

        if (file) {
            const reader = new FileReader();

            previewImage.style.display = "block";

            reader.addEventListener("load", function() {
                previewImage.setAttribute("src", this.result);
            })

            reader.readAsDataURL(file);
        }
    })
}