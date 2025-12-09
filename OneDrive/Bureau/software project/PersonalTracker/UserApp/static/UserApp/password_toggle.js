document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".toggle-password");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const input = btn.parentElement.querySelector(".password-input");

            if (!input) return;

            if (input.type === "password") {
                input.type = "text";
            } else {
                input.type = "password";
            }
        });
    });
});
