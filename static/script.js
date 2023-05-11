const $ = (query) => {
  return document.querySelector(query);
}


$("#join-form").addEventListener("submit", (e) => {
  e.preventDefault();

  fetch("/api/join", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name: $("#name").value,
      public: $("#public").value,
      private_aa: $("#private_aa").value,
      private_as: $("#private_as").value,
      private_ad: $("#private_ad").value,
      private_ss: $("#private_ss").value,
      private_ds: $("#private_ds").value,
      private_dd: $("#private_dd").value
    })
  })
  return false;
})
