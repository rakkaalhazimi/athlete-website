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