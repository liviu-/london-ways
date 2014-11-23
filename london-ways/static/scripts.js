
$(document).ready(function () {
    $('#stations-form').submit(function () {
        var $new_id = ($('#stations-select').val());
        window.location.replace('/' + $new_id);
        return false;
    });
    setTimeout(getData, 5000);
});
