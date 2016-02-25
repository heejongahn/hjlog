$(document).ready(function() {
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
    var img = document.createElement('img');
    var reader = new FileReader();

    reader.onload = function(e) {
      img.src = e.target.result;
      img.onload = function () {
        var canvas = resize(img);
        var dataURL = canvas.toDataURL('image/jpeg');
        var blob = dataURItoBlob(dataURL);
        var formData = new FormData();

        formData.append('file', blob, file.name);
        upload(formData);
      }
    }

    reader.readAsDataURL(file);
  });
});

function resize(img) {
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
  ctx = canvas.getContext('2d')
  ctx.drawImage(img, 0, 0, width, height);

  return canvas;
}

function dataURItoBlob(dataURI) {
  var byteString;
  if (dataURI.split(',')[0].indexOf('base64') >= 0) {
    byteString = atob(dataURI.split(',')[1]);
  } else {
    byteString = unescape(dataURI.split(',')[1]);
  }

  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
  var arrayBuffer = new ArrayBuffer(byteString.length);
  var intArray = new Uint8Array(arrayBuffer);

  for (var i = 0; i < byteString.length; i++) {
    intArray[i] = byteString.charCodeAt(i);
  }

  var blob = new Blob([arrayBuffer], {"type": mimeString});
  return blob;
}

function upload(formData) {
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
        updateForm(data['name'], data['url']);
      } else {
        alert("파일의 형식이 올바르지 않아요!")
      }
    },
    error: function(xhr) {
      console.log(xhr);
    }
  });
}

function updateForm(name, url) {
  var textarea = document.getElementsByTagName('textarea')[0];
  var photoNames = document.getElementsByName('photonames')[0];

  textarea.innerHTML += ('![' + name + '](' + url + ')');
  photoNames.innerHTML += (" " + name);
}
