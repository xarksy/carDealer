document.getElementById('view-grid').addEventListener('click', function() {
document.getElementById('car-container').setAttribute('data-view', 'grid');
document.querySelectorAll('.car-item').forEach(function(item) {
    item.classList.add('d-none');
    if (item.classList.contains('grid-view')) {
    item.classList.remove('d-none');
    }
});
});

document.getElementById('view-list').addEventListener('click', function() {
document.getElementById('car-container').setAttribute('data-view', 'list');
document.querySelectorAll('.car-item').forEach(function(item) {
item.classList.add('d-none');
if (item.classList.contains('list-view')) {
item.classList.remove('d-none');
}
});
});
    
function attachListeners() {        
    document.querySelectorAll('.close').forEach(function(button) {
        button.addEventListener('click', function() {
            const card = this.closest('.car-item');
            card.remove();
        });
    });        
}



window.onload = function() {
    attachListeners();      
}

    