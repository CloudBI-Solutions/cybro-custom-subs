
$(document).ready(function(){
    $(document).on('click', '.ian-cart-plus', function() {
        var qty_input = $(this).parent().parent().parent().find('.ian-popup__counter-input')
        var cur_qty = parseInt(qty_input.val())
        qty_input.val(cur_qty + 1)
    })
    $(document).on('click', '.ian-cart-minus', function() {
        var qty_input = $(this).parent().parent().parent().find('.ian-popup__counter-input')
        var cur_qty = parseInt(qty_input.val())
        cur_qty == 1 ? qty_input.val(cur_qty) : qty_input.val(cur_qty - 1)
    })
})