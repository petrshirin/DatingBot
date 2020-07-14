
const rotateParam = {
		rotated: false,
		deg: 0
	};

(async () => {
    const CANVAS_WIDTH = 852
	const CANVAS_HEIGHT = 1092

	const canvas = document.getElementsByTagName('canvas')[0]
	const context = canvas.getContext('2d')
	let originalImage = await loadImage(document.getElementsByClassName('imagePreviewImage')[0].src)
	const mouse = getMouse(canvas)
	let image = originalImage

	canvas.width = CANVAS_WIDTH
	canvas.height = CANVAS_HEIGHT

	const imageParams = {
		offsetX: 0,
		offsetY: 0,
		scale: 1
	}

	canvasUpdate()
	function canvasUpdate (time) {
    	image = originalImage
		requestAnimationFrame(canvasUpdate)

		if (mouse.left) {
			imageParams.offsetX = mouse.dx + imageParams.offsetX
			imageParams.offsetY = mouse.dy + imageParams.offsetY
		}

		if (mouse.wheel) {
			imageParams.scale += mouse.wheel * 0.1
		}

		imageParams.offsetX = Math.max(Math.min(0, imageParams.offsetX), canvas.width - image.width * Math.abs(imageParams.scale))
		imageParams.offsetY = Math.max(Math.min(0, imageParams.offsetY), canvas.height - image.height * Math.abs(imageParams.scale))

		clearCanvas()

		if (rotateParam.rotated) {
			context.translate(canvas.width/2,canvas.height/2)
			context.rotate(rotateParam.deg * 90 * Math.PI/180)
			context.translate(0, 0)
		}
		context.drawImage(
			image,
			0, 0, image.width, image.height,
			imageParams.offsetX, imageParams.offsetY, image.width * imageParams.scale, image.height * imageParams.scale
		)
		mouse.update()
	}

	function clearCanvas () {
		canvas.width = canvas.width
	}

	const loadImageElement = document.getElementById('inpFile')
	loadImageElement.addEventListener('change', async event => {
		const file = loadImageElement.files[0]
		const base64 = await getBase64(file)
		const image = new Image()

        try {
            if (file) {
                for (let i = 0; i < 2; i++) {
                    document.getElementsByClassName("btn")[i].style.display = "block";
                }
            }
        } catch (e) {
            console.log(e)
        }

            const reader = new FileReader();


		image.onload = () => {
			originalImage = image
		}
		image.src = base64
		document.getElementsByClassName('imagePreviewImage')[0].src = image.src
        document.querySelector(".photo").style.border = "none";
		document.getElementById("inpFile").style.display = "none";
	})

	const rotate = document.getElementsByClassName('rotate')[0]
	rotate.addEventListener('click', event => {
		rotateParam.rotated = true
		rotateParam.deg += 1
		if (rotateParam.deg === 4) {
			rotateParam.deg = 0
		}
		imageParams.scale = 1
	})
	const submit = document.getElementById('button')
	submit.addEventListener('click', event => {
		event.preventDefault()
		const dataURL = canvas.toDataURL('image/png').split(',')[1]
		if (window.location.href.split('/')[4] === 'addphoto') {
			const form = new FormData(document.getElementsByTagName('form')[0])
			form.delete('inpFile')
			form.append('inpFile', dataURL)
			fetch("/profile/addphoto/",
				{
					body: form,
					method: "post"
				})
				.then(function (res) {
					window.location.href = '/profile/go/'
				})
		}
		else if (window.location.href.split('/')[4] === 'my') {
			const form = new FormData(document.getElementsByTagName('form')[0])
			form.delete('inpFile')
			form.append('inpFile', dataURL)
			fetch("/profile/my/",
				{
					body: form,
					method: "post"
				})
				.then(function (res) {
					window.location.href = '/profile/search/'
				})
		}
	})


	function getBase64(file) {
		return new Promise((resolve, reject) => {
			const reader = new FileReader()
			reader.readAsDataURL(file)
			reader.onload = () => resolve(reader.result)
			reader.onerror = error => reject(error)
		});
	}


}) ()


function loadImage (src) {
	return new Promise((resolve, reject) => {
		try {
			const image = new Image
			image.onload = () => resolve(image)
			image.src = src
		} catch (err) {
			return reject(err)
		}
	})
}

function getMouse (element) {
	const mouse = {
		x: null, dx: null,
		y: null, dy: null,
		left: false, leftPrev: false,
		right: false, rightPrev: false,
		wheel: 0, wheelPrev: 0,
		wheelPx: 0, wheelPxPrev: 0
	}

	element.addEventListener('touchmove', event => {

		const rect = canvas.getBoundingClientRect()

		let x = rect.left
		let y = rect.top
		console.log(event)
		if (rotateParam.deg === 1) {
			x = x + event.changedTouches[0].clientY
			y = y - event.changedTouches[0].clientX
		}
		else if (rotateParam.deg === 2) {
			x = x - event.changedTouches[0].clientX
			y = y - event.changedTouches[0].clientY
		}
		else if (rotateParam.deg === 3) {
			x = x - event.changedTouches[0].clientY
			y = y + event.changedTouches[0].clientX
		}
		else {
			x = x + event.changedTouches[0].clientX
		    y = y + event.changedTouches[0].clientY
		}


		//const x = event.changedTouches[0].clientX - rect.left
		//const y = event.changedTouches[0].clientY - rect.top

		if (!mouse.x) {
			mouse.x = x
			mouse.y = y
			mouse.dx = 0
			mouse.dy = 0
		}
		else {
			mouse.dx = x - mouse.x
			mouse.dy = y - mouse.y

			mouse.x = x
			mouse.y = y
		}


	})

	element.addEventListener('touchstart', event => {
		console.log(event)
		mouse.left = true
    event.preventDefault()
  })

	element.addEventListener('touchend', event => {
			mouse.left = false
			mouse.x = 0
			mouse.y = 0
        event.preventDefault()
	})
	element.addEventListener('mouseup', event => {
			mouse.left = false
        event.preventDefault()
	})

	element.addEventListener('mousewheel', event => {
		console.log(event)
		mouse.wheelPxPrev = mouse.wheelPx
		mouse.wheelPrev = mouse.wheel
		mouse.wheelPx = event.deltaY
		mouse.wheel = mouse.wheelPx > 0 ? 1 : -1
		event.preventDefault()
	})

	const minusTool = document.getElementById('minusTool')
	minusTool.addEventListener('click', event => {
		console.log(event)
		mouse.wheelPxPrev = mouse.wheelPx
		mouse.wheelPrev = mouse.wheel
		mouse.wheelPx = -12
		mouse.wheel = mouse.wheelPx > 0 ? 1 : -1
		event.preventDefault()
	})

	const plusTool = document.getElementById('plusTool')
	plusTool.addEventListener('click', event => {
		console.log(event)
		mouse.wheelPxPrev = mouse.wheelPx
		mouse.wheelPrev = mouse.wheel
		mouse.wheelPx = 12
		mouse.wheel = mouse.wheelPx > 0 ? 1 : -1
		event.preventDefault()
	})


	mouse.update = () => {
		mouse.dx = 0
		mouse.dy = 0
		mouse.x = 0
		mouse.y = 0
		mouse.wheelPxPrev = mouse.wheelPx
		mouse.wheelPrev = mouse.wheel
		mouse.wheelPx = 0
		mouse.wheel = 0
	}

	return mouse
}


function dataURItoBlob(dataURI) {
	var byteString;
	if (dataURI.split(',')[0].indexOf('base64') >= 0)
		byteString = atob(dataURI.split(',')[1]);
	else
		byteString = unescape(dataURI.split(',')[1]);
	var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
	var ia = new Uint8Array(byteString.length);
	for (var i = 0; i < byteString.length; i++) {
		ia[i] = byteString.charCodeAt(i);
	}
	return [ia]
}