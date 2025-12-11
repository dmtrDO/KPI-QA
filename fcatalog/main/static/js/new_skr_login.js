
function validateForm(form) {
    form.addEventListener("submit", function(e) {

        console.log("llalal");
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        const err = document.querySelector(".login_error");
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        const passwordPattern = /^[A-Za-z0-9!@#$%^&*()\-_+=.,<>/?\[\]{}\\|`~]+$/;

        if (email.length < 4) {
            e.preventDefault();
            err.textContent = "Мінімальна довжина пошти - 4 символи !";
        }  else if (password.length < 4) {
            e.preventDefault();
            err.textContent = "Мінімальна довжина паролю - 4 символи !";
        } else if (email.length > 50) {
            e.preventDefault();
            err.textContent = "Максимальна довжина пошти - 50 символів !";
        }  else if (password.length > 50) {
            e.preventDefault();
            err.textContent = "Максимальна довжина паролю - 50 символів !";
        } else if (!emailPattern.test(email)) {
            e.preventDefault();
            err.textContent = "Невірний формат пошти !";
        } else if (!passwordPattern.test(password)) {
            e.preventDefault();
            err.textContent = "Пароль може складатись тільки з латинських малих та великих літер, цифр та символів !@#$%^&*()-_=+.,<>/?[]{}\\|~";
        }
    });
}

const form = document.querySelector(".login-form");

if (form) {
    validateForm(form);
}
