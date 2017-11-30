function optFunc() {
    var optForm = document.getElementById('more-options');
    var optButton = document.getElementById('optButton');
    if (optForm.style.display === 'none') {
        optForm.style.display = 'block';
    } else {
        optForm.style.display = 'none';
    }
}

function myFunc() {
    var change = document.getElementById('optButton');
    if (change.innerHTML=="<span><i class=\"fa fa-caret-square-o-down\" aria-hidden=\"true\"></i></span>More Options") {
        change.innerHTML = "<span><i class=\"fa fa-caret-square-o-up\" aria-hidden=\"true\"></i></span>Less Options";
    }
    else {
        change.innerHTML = "<span><i class=\"fa fa-caret-square-o-down\" aria-hidden=\"true\"></i></span>More Options";
    }
}

