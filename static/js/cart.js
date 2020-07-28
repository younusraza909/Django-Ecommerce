const updateBtns = document.querySelectorAll(".update-cart");

updateBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    var productId = btn.dataset.product;
    var action = btn.dataset.action;
    console.log("productId:", productId, "Action:", action);

    console.log("USER:", user);
    if (user === "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
});

const addCookieItem = (productId, action) => {
  console.log("User Not Logged In");

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productId]["quantity"] -= 1;
    if (cart[productId]["quantity"] <= 0) {
      console.log("cart Item Should Be Deleted");
      delete cart[productId];
    }
  }
  console.log("Cart:", cart);
  document.cookie = `cart=` + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
};

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
