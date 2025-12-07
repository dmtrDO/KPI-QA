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