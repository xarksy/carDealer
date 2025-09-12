// document.getElementById('view-grid').addEventListener('click', function() {
// document.getElementById('car-container').setAttribute('data-view', 'grid');
// document.querySelectorAll('.car-item').forEach(function(item) {
//     item.classList.add('d-none');
//     if (item.classList.contains('grid-view')) {
//     item.classList.remove('d-none');
//     }
// });
// });

// document.getElementById('view-list').addEventListener('click', function() {
// document.getElementById('car-container').setAttribute('data-view', 'list');
// document.querySelectorAll('.car-item').forEach(function(item) {
// item.classList.add('d-none');
// if (item.classList.contains('list-view')) {
// item.classList.remove('d-none');
// }
// });
// });
const openBtn = document.getElementById("openBtn");
const closeBtn = document.getElementById("closeBtn");
const popup = document.getElementById("popup");


function attachListeners() {        
    document.querySelectorAll('.close').forEach(function(button) {
        button.addEventListener('click', function() {
            const card = this.closest('.car-item');
            card.remove();
        });
    });        
}

function nextStep() {
  document.getElementById("step1").style.display = "none";
  document.getElementById("step2").style.display = "block";
}

function prevStep() {
  document.getElementById("step2").style.display = "none";
  document.getElementById("step1").style.display = "block";
}


window.onload = function() {
    attachListeners();      
}

    