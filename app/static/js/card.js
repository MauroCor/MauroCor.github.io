document.addEventListener("DOMContentLoaded", function() {
    var cardSpendForm = document.getElementById("card-spend-form");

    // Display form
    document.getElementById("card-spend-button").addEventListener("click", function() {
        resetForm(cardSpendForm);
        cardSpendForm.style.display = "block";
        // Select next month
        var nextMonth = (new Date().getMonth() + 2) % 12 || 12;
        document.querySelector('.month_buttons button[value="' + nextMonth + '"]').click();
        document.getElementById('card_spend_name').focus();
    });

    document.getElementById("cancel-cost-btn").addEventListener("click", function() {
        event.preventDefault();
        cardSpendForm.style.display = "none";
    });

    // Complete form
    document.querySelectorAll('.input_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setValue(btn, 'card_spend_fees');
        });
    });

    document.querySelectorAll('.month_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setMonth(btn, 'card_month');
        });
    });

    // Display message month required
    addSubmit(cardSpendForm, 'card_month');

    // Edit cells
    document.querySelectorAll('.item-name').forEach(function(cell) {
        cell.addEventListener('click', function() {
            setSelectedCell(cell);
        });
    });

    document.getElementById('edit-cells-btn').addEventListener('click', function() {
        oldName = setEdit();
    });

    document.getElementById('ok_edit_btn').addEventListener('click', function() {
        setOkEdit(oldName);
    });

    document.getElementById('cancel_edit_btn').addEventListener('click', function() {
        setCancelEdit(oldName);
    });

    document.querySelectorAll('.cell-card-spend-value').forEach(function(cell) {
        var id = cell.getAttribute('data-id');
        var done = localStorage.getItem(id) === 'true';
        if (done) {
            cell.classList.add('done');
        }
    });

    document.querySelectorAll('.cell-card-spend-value').forEach(function(cell) {
        cell.addEventListener('click', function() {
            setLineThrough(cell);
        });
    });
});
