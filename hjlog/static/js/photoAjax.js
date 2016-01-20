$(document).ready(function() {
  $(function() {
    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
      }
    });

    $('#photoupload').change(function() {
        var formData = new FormData();
        var file = $('#photoupload')[0].files[0];
        formData.append('file', file);
        $.ajax({
          type: 'POST',
          url: '/photoajax',
          data: formData,
          enctype: "multipart/form-data",
          contentType: false,
          processData: false,
          dataType: 'json',
          success: function(data, textStatus, jqXHR) {
            if (data['correct']) {
                $("textarea").val($("textarea").val() + '![' + data['name'] +
                    ']('+data['url']+')');
                $("input[name=photonames]").val(function(i, v) {
                    return v + " " + data['name'];
                });
            } else {
                alert("파일의 형식이 올바르지 않아요!")
            }
          },
          error: function(xhr) {
            console.log(xhr);
          }
        });
     });
  });
});
