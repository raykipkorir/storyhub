// obtaining csrftoken cookie created by Django
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");
const reactions = document.querySelectorAll(".reaction");
const icons = document.getElementById("icons");
const post_id = icons.dataset.id;

const domain = "https://storyhub.up.railway.app";

// adding event listener to like and bookmark
for (let reaction of reactions) {
  reaction.addEventListener("click", (event) => {
    const action = event.target.getAttribute("data-action");
    let url = `${domain}/${post_id}/${action}/`;

    let options = {
      method: "POST",
      headers: {
        "X-CSRFTOKEN": csrftoken,
      },
      mode: "same-origin",
    };

    // data.created - reaction is either created or deleted (true or false). data.count - no. of reactions on a post
    fetch(url, options)
      .then((res) => res.json())
      .then((data) => {
        const created = data.created;
        if (action === "bookmark") {
          created
            ? (reaction.innerHTML = `<i class="fa-solid fa-bookmark" data-action="bookmark" style="cursor: pointer;"></i>`)
            : (reaction.innerHTML = `<i class="fa-regular fa-bookmark" data-action="bookmark" style="cursor: pointer;"></i>`);
        } else if (action === "like") {
          created
            ? (reaction.innerHTML = `${data.count} <i class="fa-solid fa-heart" data-action="like" style="cursor: pointer;"></i>`)
            : (reaction.innerHTML = `${data.count} <i class="fa-regular fa-heart" data-action="like" style="cursor: pointer;"></i>`);
        }
      });
  });
}

// loading like and bookmark status on page load
window.addEventListener("DOMContentLoaded", (event) => {
  // bookmark
  let bookmark = document.getElementById("bookmark_id");
  let bookmarkUrl = `${domain}/${post_id}/bookmark/`;
  fetch(bookmarkUrl, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      data.exists
        ? (bookmark.innerHTML = `<i class="fa-solid fa-bookmark" data-action="bookmark" style="cursor: pointer;"></i>`)
        : (bookmark.innerHTML = `<i class="fa-regular fa-bookmark" data-action="bookmark" style="cursor: pointer;"></i>`);
    });

  // like
  let likeUrl = `${domain}/${post_id}/like/`;
  let like = document.getElementById("like_id");
  fetch(likeUrl, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      data.exists
        ? (like.innerHTML = `${data.count} <i class="fa-solid fa-heart" data-action="like" style="cursor: pointer;"></i>`)
        : (like.innerHTML = `${data.count} <i class="fa-regular fa-heart" data-action="like" style="cursor: pointer;"></i>`);
    });
});
