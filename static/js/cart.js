const updateBtns = document.querySelectorAll(".update-cart");

updateBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    var productId = btn.dataset.product;
    var action = btn.dataset.action;
    console.log("productId:", productId, "Action:", action);

    console.log("USER:", user);
    if (user === "AnonymousUser") {
      console.log("User Is Not Authenticated");
    } else {
      updateUserOrder(productId, action);
    }
  });
});

const updateUserOrder = (productId, action) => {
  console.log("User IS Authenticated ....Sending Data");

  //We are sending data from frontend to backend
  var url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("Data:", data);
      location.reload();
    });
};
