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
      console.log("User Is Authenticated...Sending Data");
    }
  });
});
