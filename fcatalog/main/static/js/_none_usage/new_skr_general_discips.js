
const butt_menu = document.getElementById('b_menu');
const menu = document.getElementById('menu_menu');
const pop_up_bar = document.getElementById('pop_up_bar');
const pop_up_wins = document.getElementById('pop_up_wins');

document.addEventListener('click', function(e) {
    const type_click = e.target.tagName;
    // console.log(type_click);
    if (type_click!='BUTTON') {
        pop_up_bar.style.zIndex = '-1';
        pop_up_wins.style.zIndex = '-1';
        menu.style.visibility = 'hidden';
        account.style.visibility = 'hidden';
    }
});

butt_menu.addEventListener('click', () => {
    if (menu.style.visibility=='hidden') {
        pop_up_bar.style.zIndex = '100';
        pop_up_wins.style.zIndex = '100';
        menu.style.visibility = 'visible';
        account.style.visibility = 'hidden';
    } else if (menu.style.visibility=='visible') {
        pop_up_bar.style.zIndex = '-1';
        pop_up_wins.style.zIndex = '-1';
        menu.style.visibility = 'hidden';
    } else {
        pop_up_bar.style.zIndex = '100';
        pop_up_wins.style.zIndex = '100';
        menu.style.visibility = 'visible';
        account.style.visibility = 'hidden';
    }
});




// Нове
function openPopup() {
    document.body.classList.add('lock')
    const popup = document.getElementById('popup');
    popup.classList.add('active');
    popup.addEventListener('click', (e) => {
        if (!e.target.closest('.popup__content')) {
            closePopup();
        }
    });
    console.log("allalalalal");
}

function closePopup() {
    document.querySelector(".popup").classList.remove("active");
    document.body.classList.remove('lock');
    console.log("nanannanana");
}