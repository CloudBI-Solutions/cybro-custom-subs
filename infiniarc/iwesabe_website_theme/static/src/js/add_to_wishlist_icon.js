$(document).ready(function(){
     $('.o_add_wishlist').click(function(){
        $(this).hide()
        var parent = $(this).parent()
        parent.append('<button type="button" role="button" class="btn ian-product-card__wishlist" style="background-color:#ff0000d9 !important; width:30px; height:30px; opacity:0.8; margin-top: 3px;" title="Added to Wishlist" t-att-data-product-template-id="product_id.id"> <span class="fa fa-heart" role="img" aria-label="Added to wishlist"/></button>')
    })
})

