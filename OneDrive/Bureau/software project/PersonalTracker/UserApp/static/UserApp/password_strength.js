document.addEventListener("DOMContentLoaded", function () {
    // Find all password input fields with a strength meter
    const inputs = document.querySelectorAll(".password-input");

    inputs.forEach(input => {
        const wrapper = input.closest(".wb");
        const bar = wrapper.querySelector(".strength-bar");
        const label = wrapper.querySelector(".strength-label");

        input.addEventListener("input", () => {
            const value = input.value;
            const strength = getStrength(value);

            // Update bar
            bar.style.width = strength.percent + "%";
            bar.style.backgroundColor = strength.color;

            // Update label
            label.textContent = strength.text;
            label.style.color = strength.color;
        });
    });
});


function getStrength(password) {
    let score = 0;

    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    if (score <= 1) return { percent: 20, text: "Weak", color: "#dc2626" };
    if (score === 2) return { percent: 40, text: "Weak", color: "#f97316" };
    if (score === 3) return { percent: 60, text: "Medium", color: "#ea580c" };
    if (score === 4) return { percent: 80, text: "Strong", color: "#16a34a" };

    return { percent: 100, text: "Very Strong", color: "#16a34a" };
}
