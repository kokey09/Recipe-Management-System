/* Created by Tivotal */

let btn = document.querySelector(".fa-bars");
let sidebar = document.querySelector(".sidebar");
let body = document.querySelector('body');

btn.addEventListener("click", () => {
  sidebar.classList.toggle("close");
  if (sidebar.classList.contains('close')) {
    body.style.paddingLeft = '0px';
  } else {
    body.style.paddingLeft = '268px';
  }
});

let arrows = document.querySelectorAll(".arrow");
for (var i = 0; i < arrows.length; i++) {
  arrows[i].addEventListener("click", (e) => {
    let arrowParent = e.target.parentElement.parentElement;
    arrowParent.classList.toggle("show");
  });
}


