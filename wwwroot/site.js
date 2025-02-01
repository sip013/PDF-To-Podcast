// Function to set a session storage helper
window.sessionStorageHelper = {
  setItem: function (key, value) {
    sessionStorage.setItem(key, value);
  },
  getItem: function (key) {
    return sessionStorage.getItem(key);
  },
  removeItem: function (key) {
    sessionStorage.removeItem(key);
  },
};


// Function to set a cookie
window.setCookie = function (name, value, days) {
  let expires = "";
  if (days) {
    let date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + value + ";" + expires + "; path=/";
};
window.audioElement = document.getElementById("podcastAudio");

function togglePlayPause() {
  const audioElement = document.getElementById("podcastAudio");
  if (audioElement.paused) {
      audioElement.play();
  } else {
      audioElement.pause();
  }
}