let csrfToken = document.querySelector("meta[name=csrf-token]").getAttribute("content");
let photoUploadForm = document.getElementById("photoupload");

const resize = (img) => {
  const MAX_LENGTH = 800;

  let canvas = document.createElement('canvas');
  let ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);

  let [width, height] = [img.width, img.height];
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

  [canvas.width, canvas.height] = [width, height];
  ctx = canvas.getContext('2d')
  ctx.drawImage(img, 0, 0, width, height);

  return canvas;
}


const dataURItoBlob = (dataURI) => {
  let byteString;
  if (dataURI.split(',')[0].indexOf('base64') >= 0) {
    byteString = atob(dataURI.split(',')[1]);
  } else {
    byteString = unescape(dataURI.split(',')[1]);
  }

  const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
  const arrayBuffer = new ArrayBuffer(byteString.length);
  const intArray = new Uint8Array(arrayBuffer);

  for (let i = 0; i < byteString.length; i++) {
    intArray[i] = byteString.charCodeAt(i);
  }

  return new Blob([arrayBuffer], {"type": mimeString});
}


const upload = (formData) => {
  let headers = new Headers({
    "x-requested-with": "XMLHttpRequest",
    "x-csrftoken": csrfToken,
    "accept": "application/json"
  });

  fetch("/photoajax", {
    method: "POST",
    mode: "same-origin",
    credentials: "same-origin",
    body: formData,
    headers: headers
  }).then(function(response) {
    if (!response.ok) {
      throw Error(response.statusText);
    }
    return response.json();
  }).then((data) => {
    updateForm(data["name"], data["url"]);
  }).catch((e) => {
    console.log(e);
  });
}


const updateForm = (name, url) => {
  const textarea = document.getElementsByTagName("textarea")[0];
  const photoNames = document.getElementsByName("photonames")[0];

  textarea.value = `${textarea.value}![${name}](${url})`;
  photoNames.value = `${photoNames.value} ${name}`;
}


const handleUpload = (e) => {
  const file = e.target.files[0];
  const img = document.createElement('img');
  const reader = new FileReader();

  reader.onload = (e) => {
    img.src = e.target.result;
    img.onload = () => {
      const dataURL = resize(img).toDataURL('image/jpeg');
      const blob = dataURItoBlob(dataURL);
      const formData = new FormData();

      formData.append('file', blob, file.name);
      upload(formData);
    }
  }

  reader.readAsDataURL(file);
}

if (photoUploadForm) {
  photoUploadForm.addEventListener("change", handleUpload);
}
