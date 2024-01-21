$('#modal_view_report').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var report_id = button.data('reportid');
    var modal = $(this);
    modal.find('#model_report_view_content').text("");
    $('#modal_view_report').modal('handleUpdate');

    $.get("report/view/" + report_id + "/", function(data) {
        modal.find('#model_report_view_content').text(data);
        $('#modal_view_report').modal('handleUpdate');
    });

})
