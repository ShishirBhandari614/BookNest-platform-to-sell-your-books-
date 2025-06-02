document.addEventListener("DOMContentLoaded", function () {
    const wrappers = document.querySelectorAll(".quantity-wrapper");
    const cartTotalElement = document.getElementById("cart-total");
  
    function updateCartTotal() {
      let total = 0;
      document.querySelectorAll(".item-total-amount").forEach(span => {
        const value = parseFloat(span.textContent) || 0;
        total += value;
      });
      if (cartTotalElement) {
        cartTotalElement.textContent = total.toFixed(2);
      }
  
      // Update estimated total as well
      const estimatedTotal = document.getElementById("estimated-total");
      if (estimatedTotal) {
        estimatedTotal.textContent = `Rs${total.toFixed(2)} NPR`;
      }
    }
  
    wrappers.forEach(wrapper => {
      const input = wrapper.querySelector(".qty-input");
      const plusBtn = wrapper.querySelector(".plus");
      const minusBtn = wrapper.querySelector(".minus");
      const message = wrapper.querySelector(".quantity-msg");
      const maxQuantity = parseInt(wrapper.dataset.available);
  
      // Find corresponding item-total-price by DOM traversal
      const itemRow = wrapper.closest(".cart-row");
      const itemTotalDiv = itemRow.querySelector(".item-total-price");
      const unitPrice = parseFloat(itemTotalDiv.dataset.unitPrice);
  
      function showMessage(text) {
        message.textContent = text;
        message.style.opacity = 1;
        setTimeout(() => {
          message.style.opacity = 0;
        }, 3000);
      }
  
      plusBtn.addEventListener("click", () => {
        let qty = parseInt(input.value);
        if (qty < maxQuantity) {
          qty += 1;
          input.value = qty;
          const newTotal = unitPrice * qty;
          itemTotalDiv.querySelector(".item-total-amount").textContent = newTotal.toFixed(2);
          updateCartTotal();
          message.textContent = "";
        } else {
          showMessage("Only available quantity can be added.");
        }
      });
  
      minusBtn.addEventListener("click", () => {
        let qty = parseInt(input.value);
        if (qty > 1) {
          qty -= 1;
          input.value = qty;
          const newTotal = unitPrice * qty;
          itemTotalDiv.querySelector(".item-total-amount").textContent = newTotal.toFixed(2);
          updateCartTotal();
          message.textContent = "";
        } else {
          showMessage("Quantity cannot be less than 1.");
        }
      });
    });
  });