document.addEventListener("DOMContentLoaded", function() {
    var fixedCostForm = document.getElementById("fixed-cost-form");
    var earningForm = document.getElementById("earning-form");
    var investForm = document.getElementById("invest-form");

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

    document.getElementById("invest-button").addEventListener("click", function() {
        investForm.style.display = "block";
        // Select next month
        var nextMonth = (new Date().getMonth() + 2) % 12 || 12;
        investForm.querySelector('.month_buttons button[value="' + nextMonth + '"]').click();
        document.getElementById('excess').focus();
    });

    document.getElementById("cancel-cost-btn").addEventListener("click", function() {
        event.preventDefault();
        fixedCostForm.style.display = "none";
    });

    document.getElementById("cancel-earning-btn").addEventListener("click", function() {
        event.preventDefault();
        earningForm.style.display = "none";
    });

    document.getElementById("cancel-invest-btn").addEventListener("click", function() {
        event.preventDefault();
        investForm.style.display = "none";
    });

    // Complete form
    document.querySelectorAll('.input_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setValue(btn, 'earning_name');
            setValue(btn, 'fixed_name');
        });
    });

    document.querySelectorAll('.month_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            setMonth(btn, 'earning_month');
            setMonth(btn, 'cost_month');
        });
    });

    investForm.querySelectorAll('.month_buttons button').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var oflwValue = document.querySelector('.oflw_' + btn.value).innerText;
            var balValue = document.querySelector('.bal_' + btn.value).innerText;
            investForm.querySelectorAll('.out-inv')[0].innerText = oflwValue;
            investForm.querySelectorAll('.bal-inv')[0].innerText = balValue;
            var template = investForm.querySelector('.template');
            var elementShown = false;
            investForm.querySelectorAll('.inv-summ').forEach(function(element) {
                element.classList.remove('focus');
                element.style.display = "none";
                template.style.display = "none";
                var spanMonth = element.querySelector('span');
                if (spanMonth.innerText === btn.innerText) {
                    element.style.display = "block";
                    element.classList.add('focus');
                    elementShown = true;
                }
            });
            if (!elementShown) {
                template.style.display = "block";
            } else {
                template.style.display = "none";
            }
        });
    });

    document.getElementById("save-invest-btn").addEventListener("click", function() {
        event.preventDefault();
        var month = investForm.querySelector('.month_buttons button.selected').innerText;
        var vwallet = investForm.querySelector('.out-inv').innerText;
        var total = investForm.querySelector('.tot-inv').innerText;
        var note = investForm.querySelector('#note-inv').value;
        investForm.querySelector('#month-inv').value = month;
        investForm.querySelector('#vwallet-inv').value = vwallet;
        investForm.querySelector('#total-inv').value = total;
        investForm.querySelector('#notes-inv').value = note;
        if (investForm.querySelector('.template').style.display != "none") {
            investForm.querySelectorAll('.template span')[0].innerText = month;
            investForm.querySelectorAll('.template span')[1].innerText = vwallet;
            investForm.querySelectorAll('.template span')[2].innerText = total;
            investForm.querySelectorAll('.template span')[3].innerText = note;
        } else {
            investForm.querySelectorAll('.focus span')[0].innerText = month;
            investForm.querySelectorAll('.focus span')[1].innerText = vwallet;
            investForm.querySelectorAll('.focus span')[2].innerText = total;
            investForm.querySelectorAll('.focus span')[3].innerText = note;
        }
    });

    document.getElementById("excess").addEventListener("input", function() {
        var excessInput = document.getElementById('excess').value.trim();
        var excessValue = excessInput ? parseInt(excessInput) : 0;
        var balText = document.querySelector('.bal-inv').innerText;
        var balValue = parseFloat(balText.replace(/[^\d.,-]/g, '').replace(',', '.').replace(/^(-?)(\d*)\.(.*)$/, '$1$2$3'));
        var total = balValue + excessValue;
        var formattedTotal = (total < 0 ? "-$" : "$") + Math.abs(total).toLocaleString('es-ES', { maximumFractionDigits: 0 });
        investForm.querySelector('.tot-inv').innerText = formattedTotal;
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

    // Check done cells
    document.querySelectorAll('.cell-earning-value, .cell-fixed-cost-value').forEach(function(cell) {
        var id = cell.getAttribute('data-id');
        var done = localStorage.getItem(id) === 'true';
        if (done) {
            cell.classList.add('done');
        }
    });

    document.querySelectorAll('.cell-earning-value, .cell-fixed-cost-value').forEach(function(cell) {
        cell.addEventListener('click', function() {
            setLineThrough(cell);
        });
    });
});
