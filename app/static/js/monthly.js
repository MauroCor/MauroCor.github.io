document.addEventListener("DOMContentLoaded", function() {
    var fixedCostForm = document.getElementById("fixed-cost-form");
    var earningForm = document.getElementById("earning-form");

    // Display & reset form
    document.getElementById("fixed-cost-button").addEventListener("click", function() {
        resetForm(fixedCostForm);
        fixedCostForm.style.display = "block";
        earningForm.style.display = "none";
    });

    document.getElementById("earning-button").addEventListener("click", function() {
        resetForm(earningForm);
        earningForm.style.display = "block";
        fixedCostForm.style.display = "none";
    });

    document.getElementById("cancel-cost-btn").addEventListener("click", function() {
        event.preventDefault();
        fixedCostForm.style.display = "none";
    });

    document.getElementById("cancel-earning-btn").addEventListener("click", function() {
        event.preventDefault();
        earningForm.style.display = "none";
    });

    // Complete form
    document.querySelectorAll('.input_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setValue(btn, 'earning_name');
        });
    });

    document.querySelectorAll('.input_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setValue(btn, 'fixed_name');
        });
    });

    document.querySelectorAll('.month_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setMonth(btn, 'earning_month');
        });
    });

    document.querySelectorAll('.month_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setMonth(btn, 'cost_month');
        });
    });

    // Display message month required
    addSubmit(earningForm, 'earning_month');
    addSubmit(fixedCostForm, 'cost_month');

    // Edit table
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

    document.querySelectorAll('.cell-earning-value, .cell-fixed-cost-value').forEach(function(cell) {
        cell.addEventListener('click', function() {
            setLineThrough(cell);
        });
    });
});
