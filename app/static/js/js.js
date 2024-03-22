$(document).ready(function() {
    // Fija la primera columna
    var $table = $('#fixed-columns-table');
    var $headerCell = $table.find('thead th:first-child');
    var $bodyCells = $table.find('tbody td:first-child');

    $headerCell.css('position', 'sticky');
    $headerCell.css('left', 0);
    $headerCell.css('z-index', 1);

    $bodyCells.each(function() {
        $(this).css('position', 'sticky');
        $(this).css('left', 0);
        $(this).css('z-index', 1);
    });
});