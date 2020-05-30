$(document).on('formErrors', function () {
    if (typeof formErrors === 'undefined') {
        return;
    }
    clearErrors();
    $.each(formErrors, function (field, errors) {
        $('[name="' + field + '"]').parents('.form-group').addClass('has-danger').append(
            '<small class="help-block text-error">' + errors[0] + '</small>'
        );
    });
});

function clearErrors() {
    var displayedErrors = $("small.text-error");
    $.each(displayedErrors, function (id, small) {
        $(small).remove();
    });
}
$(document).ready(function () {
    $(document).trigger('formErrors');
});