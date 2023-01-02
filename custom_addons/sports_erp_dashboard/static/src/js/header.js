var MenuToggle = $("#se-menu-toggle");
MenuToggle.click(function(e){
   e.preventDefault();
   $('.se-sidebar').toggleClass('se-sidebar--show')
})