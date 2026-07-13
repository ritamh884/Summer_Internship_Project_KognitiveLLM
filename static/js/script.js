// ===============================
// AI Financial Analyzer
// Login Page JavaScript
// ===============================

// Show / Hide Password
function togglePassword() {

    const password = document.getElementById("password");
    const toggle = document.querySelector(".toggle-password");

    if (password.type === "password") {

        password.type = "text";
        toggle.innerHTML = "🙈";

    } else {

        password.type = "password";
        toggle.innerHTML = "👁";

    }
}


// Login Button Animation
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const loginBtn = document.querySelector(".login-btn");

    form.addEventListener("submit", function () {

        loginBtn.disabled = true;
        loginBtn.innerHTML = "Logging in...";

    });

});


// Input Focus Effect
const inputs = document.querySelectorAll("input");

inputs.forEach(input => {

    input.addEventListener("focus", function () {

        this.style.boxShadow = "0 0 10px rgba(56,189,248,0.5)";

    });

    input.addEventListener("blur", function () {

        this.style.boxShadow = "none";

    });

});