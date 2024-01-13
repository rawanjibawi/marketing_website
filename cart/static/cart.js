console.log("hello cart");
function decrementQuantity(cartItemId) {
  // AJAX request to decrement the quantity
  $.ajax({
    type: "POST",
    url: '{% url "cart:decrement_quantity" 0 %}'.replace("0", cartItemId),
    data: {
      csrfmiddlewaretoken: "{{ csrf_token }}",
    },
    dataType: "json",
    success: function (response) {
      if (response.success) {
        // Update the UI with the new quantity and total price per item
        const quantityElement = document.getElementById(
          "quantity_" + cartItemId
        );
        const totalPriceElement = document.getElementById(
          "total_price_" + cartItemId
        );

        if (quantityElement && totalPriceElement) {
          quantityElement.innerHTML = response.quantity;
          totalPriceElement.innerHTML = response.total_price_per_item + "$";
        }
      } else {
        console.error(response.message);
      }
    },
    error: function (error) {
      console.error("Error:", error);
    },
  });
}
