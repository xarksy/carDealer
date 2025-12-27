window.addEventListener('DOMContentLoaded', function () {
    // ==========================================
    // BAGIAN 1: LOGIKA KALKULATOR KREDIT
    // ==========================================
    const cashInput = document.getElementById('cash');
    const tenorInput = document.getElementById('tenor');
    const interestInput = document.getElementById('interest');

    const calculateButton = document.getElementById('hitung');
    const resetButton = document.getElementById('reset_hitungan');

    const angsuranBulanan = document.getElementById('angsuran_bulanan');
    const totalPembayaran = document.getElementById('total_pembayaran');
    const totalBunga = document.getElementById('total_bunga');

    if (calculateButton) {
        calculateButton.addEventListener('click', function(event) {
            event.preventDefault();

            const cash = parseFloat(cashInput.value.replace(/,/g,'')) || 0;
            const tenor = parseInt(tenorInput.value) || 0;
            const interest = parseFloat(interestInput.value) || 0;

            if (cash && tenor && interest) {
                const monthlyInterestRate = interest / 100 / 12;
                const monthlyPayment = (cash * monthlyInterestRate) / (1 - Math.pow(1 + monthlyInterestRate, -tenor));
                const totalPayment = monthlyPayment * tenor;
                const totalInterest = totalPayment - cash;

                angsuranBulanan.innerText = `Rp${monthlyPayment.toLocaleString('id-ID')}`;
                totalPembayaran.innerText = `Rp${totalPayment.toLocaleString('id-ID')}`;
                totalBunga.innerText = `Rp${totalInterest.toLocaleString('id-ID')}`;
            }
        });
    }

    if (resetButton) {
        resetButton.addEventListener('click', function () {
            cashInput.value = '';
            tenorInput.value = ''; 
            angsuranBulanan.innerText = '-';
            totalPembayaran.innerText = '-';
            totalBunga.innerText = '-';
        });
    }

    // ==========================================
    // BAGIAN 2: LOGIKA POP-UP / MODAL OTOMATIS
    // ==========================================
    
    // Cek apakah jQuery ($) sudah dimuat
    if (typeof $ !== 'undefined') {
        // Cek apakah elemen modal ada di halaman
        var $modal = $('#successModal');
        
        if ($modal.length > 0) {
            console.log("Modal ditemukan! Memunculkan pop-up..."); // Cek Console browser (F12) jika tidak muncul
            $modal.modal('show');
        } else {
            console.log("Tidak ada pesan sukses (Modal tidak dirender).");
        }
    } else {
        console.error("jQuery belum dimuat! Pastikan script jQuery ada di atas script ini.");
    }
});