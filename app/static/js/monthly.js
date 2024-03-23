document.addEventListener("DOMContentLoaded", function() {
    var fixedCostForm = document.getElementById("fixed-cost-form");
    var earningForm = document.getElementById("earning-form");

    document.getElementById("fixed-cost-button").addEventListener("click", function() {
        fixedCostForm.style.display = "block";
    });

    document.getElementById("cancel-cost-btn").addEventListener("click", function() {
        fixedCostForm.style.display = "none";
    });

    document.getElementById("earning-button").addEventListener("click", function() {
        earningForm.style.display = "block";
    });

    document.getElementById("cancel-earning-btn").addEventListener("click", function() {
        earningForm.style.display = "none";
    });
});
