document.addEventListener("DOMContentLoaded", function() {
    var bodyCells = document.getElementById('fixed-columns-table').querySelectorAll('tbody td:not(:first-child):not(.delete-button)');

    // Money format
    bodyCells.forEach(function(cell) {
        var cellText = cell.textContent.trim();
        var cellNumber = parseFloat(cellText.replace(/[^\d]/g, ''));
        if (isNaN(cellNumber)) {
            cell.textContent = '';
        } else {
            var formattedNumber = "$" + cellNumber.toLocaleString('es-ES', { maximumFractionDigits: 0 });
            cell.textContent = formattedNumber;
        }
    });
});

function setValue(btn, inputId) {
    var value = btn.value;
    var input = document.getElementById(inputId);
    var prevSelectedButton = document.querySelector('.input_buttons button.selected');

    if (prevSelectedButton) {
        prevSelectedButton.classList.remove('selected');
    }

    if (!btn.classList.contains('selected')) {
        btn.classList.add('selected');
        input.value = value;
    }
}

function setMonth(btn, inputId) {
    var month = btn.value;
    var input = document.getElementById(inputId);
    var prevSelectedButton = document.querySelector('.month_buttons button.selected');
    var span = document.getElementById(inputId + '_error');

    if (prevSelectedButton) {
        prevSelectedButton.classList.remove('selected');
    }

    if (!btn.classList.contains('selected')) {
        btn.classList.add('selected');
        input.value = month;
        span.style.display = 'none';
    }
}

function resetForm(form) {
    var monthSelected = form.querySelector('.month_buttons button.selected');
    var nameSelected = form.querySelector('.input_buttons button.selected');
    form.reset();
    if (monthSelected) {
        monthSelected.classList.remove('selected');
        form.querySelector('.month_buttons input').removeAttribute('value');}
    if (nameSelected) {
        nameSelected.classList.remove('selected');}
    form.querySelector('.error-message').style.display = "none";
    form.style.display = "none";
}

function addSubmit(form, id) {
    form.addEventListener("submit", function() {
        if (!document.getElementById(id).value) {
            event.preventDefault();
            form.querySelector('.error-message').style.display = "block";
        }
    });
}