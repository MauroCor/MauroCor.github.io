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

// Edit cells section
var editingMode = false;

function setSelectedCell(cell) {
    var editBtn = document.getElementById('edit-cells-btn');
    if (!editingMode) {
        var selectedCell = document.querySelector('.item-name.selected');
        if (selectedCell && selectedCell !== cell) {
            selectedCell.classList.remove('selected');
        }
        if (!cell.classList.contains('editing')) {
            cell.classList.toggle('selected');
            editBtn.style.display = cell.classList.contains('selected') ? 'inline-block' : 'none';
        }
    }
}

function setEdit() {
    var selectedCell = document.querySelector('.item-name.selected');
    var editBtn = document.getElementById('edit-cells-btn');
    var okEditBtn = document.getElementById('ok_edit_btn');
    var cancelEditBtn = document.getElementById('cancel_edit_btn');
    if (!editingMode) {
        editingMode = true;
        selectedCell.contentEditable = true;
        selectedCell.focus();
        selectedCell.classList.add('editing');
        okEditBtn.style.display = 'inline-block';
        cancelEditBtn.style.display = 'inline-block';
        editBtn.style.display = 'none';
    }
    return selectedCell.textContent.trim();
}

function setOkEdit(oldName) {
    var selectedCell = document.querySelector('.item-name.selected');
    var okEditBtn = document.getElementById('ok_edit_btn');
    var cancelEditBtn = document.getElementById('cancel_edit_btn');
    var newName = selectedCell.textContent.trim();
    var feature = /cell-(.*?)-name/.exec(selectedCell.classList[0])[1];
    fetch(`/edit-${feature}/${encodeURIComponent(oldName)}/${encodeURIComponent(newName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
                editingMode = false;
                selectedCell.contentEditable = false;
                selectedCell.classList.remove('editing');
                selectedCell.classList.remove('selected');
                okEditBtn.style.display = 'none';
                cancelEditBtn.style.display = 'none';
            } else {
                alert(data.err_msg);
            }
        });
}

function setCancelEdit(oldName) {
    var selectedCell = document.querySelector('.item-name.selected');
    editingMode = false;
    selectedCell.contentEditable = false;
    selectedCell.textContent = oldName;
    selectedCell.classList.remove('editing');
    document.getElementById('ok_edit_btn').style.display = 'none';
    document.getElementById('cancel_edit_btn').style.display = 'none';
    document.getElementById('edit-cells-btn').style.display = 'inline-block';
}

function setLineThrough(cell) {
    var isLineThrough = cell.style.textDecoration === 'line-through';
    if (!isLineThrough) {
        cell.style.color = '#708090';
        cell.style.textDecoration = 'line-through';
    } else {
        cell.style.color = '';
        cell.style.textDecoration = '';
    }
}