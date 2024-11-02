function addProductToCart(productId, addToCartUrl){
  console.log("product id", productId);
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
    type: 'POST',
    url: addToCartUrl,
    data: {
        'product_id': productId,
        'csrfmiddlewaretoken': csrfToken
    },
    success: function(response) {


       // alert(response.message);
        $(".tag__cart").html(response.totalCartItems)
        const button = $(`#addtocart-${productId}`);
        // Update button text and style in one step
        button.text('Added to Cart')
        .removeClass('btn--secondary')
        .addClass('btn--success addedToCartSuccess')
        .prop('disabled', true);

      //  openCartModal();
    },
    error: function(xhr, status, error) {
      // Handle error - if not logged in or other issues
      if (xhr.status === 401) {
          // alert('You need to login to add items to your cart.');
          // Optionally redirect to the login page
          window.location.href = 'users/login/';
      } else {
          alert('Something went wrong: ' + error);  // General error message
      }
  }

  });
}

function openCartModal() {
  $.ajax({
      type: 'GET',
      url: 'cart/get_cart/',
      success: function(response) {
          $('#cartContents').html(response);
          $('#cartModal').removeClass('hidden');
      }
  });
}

// Close the cart modal
$('.close-modal').on('click', function() {
  $('#cartModal').addClass('hidden');
});
