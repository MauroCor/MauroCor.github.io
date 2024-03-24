$(document).ready(function() {
    // Fix first column
    var $table = $('#fixed-columns-table');
    var $headerCell = $table.find('thead th:first-child');
    var $firstColumn = $table.find('tbody td:first-child');
    var $bodyCells = $table.find('tbody td:not(:first-child, .delete-button)');

    $headerCell.css('position', 'sticky');
    $headerCell.css('left', 0);
    $headerCell.css('z-index', 1);

    $firstColumn.each(function() {
        $(this).css('position', 'sticky');
        $(this).css('left', 0);
        $(this).css('z-index', 1);
    });

    // Money format
    $bodyCells.each(function() {
        var cellText = $(this).text();
        var cellNumber = parseFloat(cellText.replace(/[^\d]/g, ''));
        if (isNaN(cellNumber)) {cellNumber = '';}
        if (cellNumber != '') {
            var formattedNumber = "$" + cellNumber.toLocaleString('es-ES', { maximumFractionDigits: 0 });
            $(this).text(formattedNumber);
        }
    });
});