window.addEventListener('DOMContentLoaded', function () {
    const cashInput = document.getElementById('cash');
    const tenorInput = document.getElementById('tenor');
    const interestInput = document.getElementById('interest');

    const  calculateButton = document.getElementById('hitung');
    const resetButton = document.getElementById('reset_hitungan');

    const angsuranBulanan = document.getElementById('angsuran_bulanan');
    const totalPembayaran = document.getElementById('total_pembayaran');
    const totalBunga = document.getElementById('total_bunga');

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

            angsuranBulanan.innerText = `Rp${monthlyPayment.toLocaleString()}`;
            totalPembayaran.innerText = `Rp${totalPayment.toLocaleString()}`;
            totalBunga.innerText = `Rp${totalInterest.toLocaleString()}`;


        }
    });

    resetButton.addEventListener('click', function () {
        cashInput.value = '';
        tenorInput.value = 12;
        angsuranBulanan.innerText = '-';
        totalPembayaran.innerText = '-';
        totalBunga.innerText = '-';
    })
})