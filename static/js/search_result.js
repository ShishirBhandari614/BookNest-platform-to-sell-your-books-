document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const query = params.get('search');

    if (query) {
        fetch(`/search-books/?search=${query}`)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById("search-results");
                container.classList.add("book-grid");
                
                if (data.length === 0) {
                    container.innerHTML = "<p>No results found.</p>";
                } else {
                    container.innerHTML = "";
                    data.forEach(book => {
                        // Create the book card HTML based on the book data
                        let bookCardHTML = `
                            <div class="book-card">
                                <img src="${book.book_cover}" alt="${book.book_name}">
                                <div class="book-info">
                                    <h3>${book.book_name}</h3>
                                    <p class="author">Author: ${book.author}</p>
                                    <p class="price">Rs ${book.book_price} NPR</p>`;
                        
                        // Add buttons based on sold status from the API response
                        if (book.sold) {
                            bookCardHTML += `<button class="sold-out" disabled>Sold out</button>`;
                        } else {
                            bookCardHTML += `
                                <a href="#" class="add-to-cart" 
                                    data-book-id="${book.id}"
                                    data-book-name="${book.book_name}"
                                    data-book-cover="${book.book_cover}">
                                    Add to cart
                                </a>
                                <a href="/buy-book/${book.id}/" class="buy-now">Buy Now</a>`;
                        }
                        
                        bookCardHTML += `
                                </div>
                            </div>`;
                        
                        container.innerHTML += bookCardHTML;
                    });
                    
                    // Initialize add to cart buttons after adding to DOM
                    initAddToCart();
                }
            })
            .catch(error => {
                console.error('Error fetching books:', error);
                document.getElementById("search-results").innerHTML = "<p>Something went wrong. Please try again later.</p>";
            });
    }
});