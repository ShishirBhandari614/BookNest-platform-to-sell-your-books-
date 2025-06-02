document.addEventListener("click", function (e) {
    if (e.target.classList.contains("add-to-cart")) {
      e.preventDefault();
  
      const csrftoken = getCookie('csrftoken');
      const cartPopup = document.getElementById('cartPopup');
  
      // Get book data from clicked element
      const bookId = e.target.getAttribute('data-book-id');
      const bookName = e.target.getAttribute('data-book-name');
      const bookCover = e.target.getAttribute('data-book-cover');
      const condition = e.target.getAttribute('data-book-condition');

  
      fetch("/add-to-cart/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          book_id: bookId,
          quantity: 1,
        }),
      })
      .then(response => response.json())
      .then(data => {
        showCartPopup({
          title: bookName,
          cover: bookCover,
          condition: condition,
          cartCount: data.cart_count
        });
        localStorage.setItem('cartCount', data.cart_count);
        // Add this line to update navbar counter
        document.getElementById('navbar-cart-count').textContent = data.cart_count;
      })
      .catch(error => {
        console.error("Error:", error);
        alert("Error adding book to cart.");
      });
    }
  });
  
  // Popup close handlers
  document.querySelector('.popup .close').addEventListener('click', closeCartPopup);
  document.getElementById('continueShoppingBtn').addEventListener('click', function(e) {
    e.preventDefault();
    closeCartPopup();
  });
  
  function showCartPopup(bookData) {
    const cartPopup = document.getElementById('cartPopup');
    document.getElementById('popup-book-image').src = bookData.cover;
    document.getElementById('popup-book-title').textContent = bookData.title;
    document.getElementById('popup-book-condition').textContent = bookData.condition || "Condition not specified";
    document.getElementById('cart-item-count').textContent = bookData.cartCount;
    cartPopup.classList.remove('hidden');
  
    setTimeout(() => {
      closeCartPopup();
    }, 5000);
  }
  
  
  function closeCartPopup() {
    document.getElementById('cartPopup').classList.add('hidden');
  }
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  