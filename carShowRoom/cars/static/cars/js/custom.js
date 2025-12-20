/* static/cars/js/custom.js */

document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Mempercantik Input Django (Tambah class Bootstrap)
    var inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(function(input) {
        // Cek agar tidak menimpa checkbox/radio/submit
        if (!input.classList.contains('form-control') && input.type !== 'checkbox' && input.type !== 'radio' && input.type !== 'submit') {
            input.classList.add('form-control');
        }
    });

    // 2. Logika Stepper Trade-In
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const btnNext = document.getElementById('btn-next');
    const btnPrev = document.getElementById('btn-prev');

    // Pastikan elemen ada sebelum menjalankan event listener
    if (step1 && step2 && btnNext && btnPrev) {
        
        btnNext.addEventListener('click', function() {
            // Sembunyikan Step 1, Tampilkan Step 2
            step1.style.display = 'none';
            step2.style.display = 'block';
            
            // Scroll sedikit ke area form agar user fokus
            document.getElementById('trade-in-section').scrollIntoView({behavior: 'smooth'});
        });

        btnPrev.addEventListener('click', function() {
            // Sembunyikan Step 2, Tampilkan Step 1
            step2.style.display = 'none';
            step1.style.display = 'block';
        });
    }
});