document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.querySelectorAll(".delete-btn");
  
    deleteButtons.forEach(button => {
      button.addEventListener("click", function() {
        const bookId = this.getAttribute("data-book-id");
        if (!bookId) return;
  
        // Removed confirmation prompt
  
        fetch(`/cart/remove/${bookId}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept': 'application/json',
          },
          credentials: 'same-origin'
        })
        .then(response => {
          if (response.status === 204) {
            this.closest('.cart-item').remove();
            
            location.reload();
            
          } else if (response.status === 404) {
            alert("Item not found in cart.");
          } else {
            alert("Failed to remove item.");
          }
        })
        .catch(error => {
          console.error("Error:", error);
          alert("An error occurred.");
        });
      });
    });
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });