const easyMDE = new EasyMDE({
  element: document.getElementById("postContent"),
});

let image = document.getElementById("output");
let labelFileInput = document.getElementById("labelFileInput");
let fileInput = document.getElementById("fileInput");
let removeCoverImage = document.getElementById("removeCoverImage");
let postTitle = document.getElementById("postTitle");
let postContent = document.getElementById("postContent");
let postForm = document.getElementById("postForm");
let imageUrl;

// retrieving local storage data on page load
document.addEventListener("DOMContentLoaded", (event) => {
  loadContent(event);
});

function loadContent(event) {
  postTitle.innerHTML = localStorage.getItem("postTitle");
  postContent.innerHTML = easyMDE.value(
    JSON.parse(localStorage.getItem("postContent"))
  );
  document.removeEventListener("DOMContentLoaded", loadContent);
}

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
  fileInput.value = "";
  localStorage.setItem("cover_pic", "");
  removeCoverImage.style.display = "none";
}

// setting title and content data on local storage
postTitle.addEventListener("change", (event) => {
  handlePostTitleChange(event);
});
function handlePostTitleChange(event) {
  localStorage.setItem("postTitle", event.target.value);
}
easyMDE.codemirror.on("change", () => {
  handlePostContentChange();
});

function handlePostContentChange() {
  localStorage.setItem("postContent", JSON.stringify(easyMDE.value()));
}

// form submission
postForm.addEventListener("submit", (event) => {
  localStorage.clear();
});
