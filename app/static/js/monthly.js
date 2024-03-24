document.addEventListener("DOMContentLoaded", function() {
    var fixedCostForm = document.getElementById("fixed-cost-form");
    var earningForm = document.getElementById("earning-form");

    document.getElementById("fixed-cost-button").addEventListener("click", function() {
        fixedCostForm.style.display = "block";
        earningForm.style.display = "none";});

    document.getElementById("cancel-cost-btn").addEventListener("click", function() {
        event.preventDefault();
        fixedCostForm.style.display = "none";});

    document.getElementById("earning-button").addEventListener("click", function() {
        earningForm.style.display = "block";
        fixedCostForm.style.display = "none";});

    document.getElementById("cancel-earning-btn").addEventListener("click", function() {
        event.preventDefault();
        earningForm.style.display = "none";});

    earningForm.addEventListener("submit", function(event) {
        var earnMonthInput = document.getElementById('earning_month');
        if (!earnMonthInput.value) {
            event.preventDefault();
            document.getElementById('earn-month-error').textContent = 'Please select a month.';
        }});
    fixedCostForm.addEventListener("submit", function(event) {
        var costMonthInput = document.getElementById('fixed_month');
        if (!costMonthInput.value) {
            event.preventDefault();
            document.getElementById('cost-month-error').textContent = 'Please select a month.';
        }});
});

function setMonthValue(btn) {
    var month = btn.value;
    var costMonthInput = document.getElementById('fixed_month');
    var earnMonthInput = document.getElementById('earning_month');
    var prevSelectedButton = document.querySelector('.month_buttons button.selected');
    var earnMonthError = document.getElementById('earn-month-error');
    var costMonthError = document.getElementById('cost-month-error');

    if (prevSelectedButton) {
        prevSelectedButton.classList.remove('selected');}

    if (!btn.classList.contains('selected')) {
        btn.classList.add('selected');
        costMonthInput.value = month;
        earnMonthInput.value = month;
        earnMonthError.textContent = '';
        earnMonthError.style.display = 'none';
        costMonthError.textContent = '';
        costMonthError.style.display = 'none';
    } else {
        btn.classList.remove('selected');
        costMonthInput.value = '';
        earnMonthInput.value = '';
    }
}

function setNameValue(btn) {
    var name = btn.value;
    var costNameInput = document.getElementById('fixed_name');
    var earnNameInput = document.getElementById('earning_name');
    var prevSelectedButton = document.querySelector('.name_buttons button.selected');

    if (prevSelectedButton) {
        prevSelectedButton.classList.remove('selected');}

    if (!btn.classList.contains('selected')) {
        btn.classList.add('selected');
        costNameInput.value = name;
        earnNameInput.value = name;
    } else {
        btn.classList.remove('selected');
        costNameInput.value = '';
        earnNameInput.value = '';
    }
}