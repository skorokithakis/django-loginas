'use strict';

django.jQuery(document).ready(function()
{
    var $ = django.jQuery;
    var reasonRequired = $('#loginas-modal').data('reason-required') === true;

    $('#loginas-link').click(function()
    {
        $('#loginas-modal').show();
        $('#loginas-reason').val('').removeClass('loginas-invalid').focus();
        $('#loginas-error').hide();
        return false;
    });

    $('#loginas-cancel, #loginas-modal-backdrop').click(function()
    {
        $('#loginas-modal').hide();
    });

    $('#loginas-confirm').click(function()
    {
        var reason = $('#loginas-reason').val().trim();
        if (reasonRequired && !reason) {
            $('#loginas-reason').addClass('loginas-invalid');
            $('#loginas-error').show();
            $('#loginas-reason').focus();
            return;
        }
        $('#loginas-reason-input').val(reason);
        $('#loginas-form').submit();
    });

    $('#loginas-reason').on('input', function()
    {
        if ($(this).val().trim()) {
            $(this).removeClass('loginas-invalid');
            $('#loginas-error').hide();
        }
    });

    $('#loginas-reason').keydown(function(e)
    {
        if (e.key === 'Escape') {
            $('#loginas-modal').hide();
        }
    });

    $('#loginas-modal-dialog').keydown(function(e)
    {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            $('#loginas-confirm').click();
        }
    });
});
