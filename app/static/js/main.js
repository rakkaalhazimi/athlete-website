function openNewTab(link) {
	window.open(link, "_blank")
}

function change_form(obj) {
	let formId = obj.getAttribute("btn-for")
	let formObjs = document.getElementsByClassName("form-list")
	let formBtns = document.getElementsByClassName("form-list-button")

	for (form of formObjs) {
		if (form.id == formId) {
			form.style.display = "block"
		} else {
			form.style.display = "none"
		}
	}

	for (btn of formBtns) {
		if (btn.getAttribute("btn-for") == formId) {
			btn.classList.add("active")
		} else {
			btn.classList.remove("active")
		}
	}
}


function sendText(obj, action) {
	var editorId = obj.getAttribute("btn-for")
	var editor = editors[editorId]
	var content = editor.getValue()

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {

		// When receive OK status from API
		if (this.readyState == 4 && this.status == 200) {
			// Restore all changes when finish
		}

		// Else, show the loading image
		// and disable the button.
		else {
		}

	}

	var req_data = {}
	req_data[editorId] = content
	var req_json = JSON.stringify(req_data)

	xhttp.open("POST", action, true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(req_json);

}