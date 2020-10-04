let selectedLi;

nav.onclick = function(event) {
    let target = event.target;
    if(target.tagName!='LI') return;
    activeMenu(target);
};

function activeMenu(il) {
    selectedLi = li;
    selectedLi.classList.add('active')
}