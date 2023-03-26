const easyMDE = new EasyMDE({
  element: document.getElementById("postContent"),
});

let image = document.getElementById("output");
let fileInput = document.getElementById("fileInput");
let removeCoverImage = document.getElementById("removeCoverImage");
let imageUrl;

// uploading cover image
fileInput.addEventListener("change", (event) => {
  handleUploadFile(event);
});

function handleUploadFile(event) {
  imageUrl = URL.createObjectURL(event.target.files[0]);
  image.src = imageUrl;
  removeCoverImage.style.display = "inline-block";
}

// removing cover image
removeCoverImage.addEventListener("click", (event) => {
  handleRemoveFile(event);
});

function handleRemoveFile(event) {
  image.src = "";
  URL.revokeObjectURL(imageUrl);
  removeCoverImage.style.display = "none";
}
