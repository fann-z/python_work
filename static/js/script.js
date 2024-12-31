document.addEventListener("DOMContentLoaded", () => {
    const url = window.location.origin;
    const accessUrl = document.getElementById("access-url");
    accessUrl.textContent = url;
    accessUrl.href = url;
});
