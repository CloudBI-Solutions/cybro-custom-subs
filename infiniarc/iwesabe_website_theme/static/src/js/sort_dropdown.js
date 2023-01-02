odoo.define('iwesabe_website_theme.sort_drop', function (require) {
    $("#dropdownMenuButton1").mouseover(function(){
      console.log('Hello')
      var menu = $(this).parent().find('.dropdown-menu')
      menu.show()
    });
    $(".dropdown-menu").mouseleave(function(){
       $(this).hide()
    });
})