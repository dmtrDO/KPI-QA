const butt_menu = document.getElementById('b_menu');
const butt_account = document.getElementById('b_account');
const menu = document.getElementById('menu_menu');
const account = document.getElementById('menu_account');

butt_menu.addEventListener('click', () => {
    if (menu.style.visibility=='hidden') {
        menu.style.visibility = 'visible';
    } else if (menu.style.visibility=='visible') {
        menu.style.visibility = 'hidden';
    } else {
        menu.style.visibility = 'visible';
    }
});
butt_account.addEventListener('click', () => {
    if (account.style.visibility=='hidden') {
        account.style.visibility = 'visible';
    } else if (account.style.visibility=='visible') {
        account.style.visibility = 'hidden';
    } else {
        account.style.visibility = 'visible';
    }
});



function validateForm(form) {
    form.addEventListener("submit", function(e) {

        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        const err = document.querySelector(".login-error");
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

const form = document.getElementById("login-form");

if (form) {
    validateForm(form);
}

function openPopup() {
    document.body.classList.add('lock')
    const popup = document.getElementById('popup');
    popup.classList.add('active');
    popup.addEventListener('click', (e) => {
        if (!e.target.closest('.popup__content')) {
            closePopup();
        }
    })
}

function closePopup() {
    document.querySelector(".popup").classList.remove("active");
    document.body.classList.remove('lock');
}

let fuse;
const input = document.getElementById("input_search");
const resultsContainer = document.getElementById("disciplines_container");

if (input) {
    fuse = new Fuse(disciplines, {
        keys: ["teacher", "title", "description"],
        includeScore: true,
        threshold: 0.4
    });
    document.getElementById("search").addEventListener("click", searchDisciplines);
}

function searchDisciplines() {
    const query = input.value.trim();
    let results;

    if (query === "") {
        results = disciplines;
    } else {
        results = fuse.search(query, { limit: disciplines.length })
            .sort((a, b) => a.score - b.score)
            .map(r => r.item);
    }

    renderResults(results);
}

function renderResults(list) {
    resultsContainer.innerHTML = "";
    list.forEach(item => {
        const block = document.createElement("div");
        block.innerHTML = `
            <p>${item.teacher}</p>
            <p>${item.title}</p>
            <p>${item.description}</p>
            <hr>
        `;
        resultsContainer.appendChild(block);
    });
}


