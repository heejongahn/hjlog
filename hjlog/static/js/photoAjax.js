function dataURItoBlob(dataURI) {
  var byteString;
  if (dataURI.split(',')[0].indexOf('base64') >= 0)
    byteString = atob(dataURI.split(',')[1]);
  else
    byteString = unescape(dataURI.split(',')[1]);

  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  var bb = new Blob([ab], {"type": mimeString});
  return bb;
}


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
    var file = $('#photoupload')[0].files[0];
    var filename = file.name;
    console.log(filename);
    var img = document.createElement('img');
    var reader = new FileReader();
    var dataURL = null;

    reader.onload = function(e)
    {
      img.src = e.target.result;

      img.onload = function () {
        console.log("image load");

        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);

        var MAX_LENGTH = 800;
        var width = img.width;
        var height = img.height;

        if (height > width) {
          if (MAX_LENGTH < height) {
            width *= MAX_LENGTH/height;
            height = MAX_LENGTH;
          }
        } else {
          if (MAX_LENGTH < width) {
            height *= MAX_LENGTH/width;
            width = MAX_LENGTH;
          }
        }
        canvas.width = width;
        canvas.height = height;
        var ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, width, height);

        dataURL = canvas.toDataURL('image/jpeg');
        var blob = dataURItoBlob(dataURL);
        var formData = new FormData();

        formData.append('file', blob, filename);

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
      }
    }
    reader.readAsDataURL(file);
   });
  });
});
