const urlParams = new URLSearchParams(window.location.search)
const msg = urlParams.get('msg')

const txt_mensaje = document.getElementById("texto")
const btn_principal = document.getElementById("btn_principal")

btn_principal.addEventListener("click", () => {
    document.location.href = "../../index.html"
})

if (msg) {
    txt_mensaje.innerHTML = msg
}