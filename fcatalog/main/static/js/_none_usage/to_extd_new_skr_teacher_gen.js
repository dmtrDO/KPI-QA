
const butt_menu = document.getElementById('b_menu');
const butt_account = document.getElementById('b_account');
const menu = document.getElementById('menu_menu');
const account = document.getElementById('menu_account');
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
butt_account.addEventListener('click', () => {
    if (account.style.visibility=='hidden') {
        pop_up_bar.style.zIndex = '100';
        pop_up_wins.style.zIndex = '100';
        account.style.visibility = 'visible';
        menu.style.visibility = 'hidden';
    } else if (account.style.visibility=='visible') {
        pop_up_bar.style.zIndex = '-1';
        pop_up_wins.style.zIndex = '-1';
        account.style.visibility = 'hidden';
    } else {
        pop_up_bar.style.zIndex = '100';
        pop_up_wins.style.zIndex = '100';
        account.style.visibility = 'visible';
        menu.style.visibility = 'hidden';
    }
});




// Для блоків
