odoo.define('iwesabe_website_theme.gearstore', function (require) {

	var ajax = require('web.ajax');

	var scrolls = document.getElementsByClassName('gearstore_component');
	console.log(scrolls,'scrolls')
    for (const scroll of scrolls) {
                if(scroll.classList.contains('active')){
                    scroll.classList.remove("active");
                    break;
                }
            }

$(".ial-filter__comp-title").click(function(e){
     e.preventDefault();
       let contentEl = e.target.parentElement.children[1];
       console.log('contentEl', contentEl);
       e.target.classList.toggle('ial-filter__comp-title--show');
       contentEl.classList.toggle('d-none');

});
$(".ial-filter__mob-icon").click(function(e){
      e.preventDefault();
      console.log('jlkjlkjljljlk');
      let mobFilterEl = document.querySelector('.ial-filter-container');
      mobFilterEl.classList.remove('ial-filter-container--resp-hide')
});
$(".close_gear_filter_mob").click(function(e){
      e.preventDefault();
      console.log('closeeeee');
      let mobFilterEl = document.querySelector('.ial-filter-container');
      mobFilterEl.classList.remove('ial-filter-container--resp-hide');
});


	$(document).ready(function(){


	    $(".footer-link-title").click(function(e){
	        e.preventDefault();
	        var linksContainer = e.target.parentElement.children[1];
	        var downArrow = e.target.children[0];
	        console.log('e.target', e.target.parentElement)
	        console.log('e.target13333', e.target)
	        console.log('downArrow', downArrow)
	        var upArrow = e.target.children[1];

	        linksContainer.classList.toggle('d-none');
	        if(linksContainer.classList.contains('d-none')){
	            downArrow.classList.remove('d-none');
	            upArrow.classList.add('d-none');
	        }else{
	            downArrow.classList.add('d-none');
	             upArrow.classList.remove('d-none');
	        }
	    })
	;})

    $(document).ready(function () {
                $(".ia-carousel").owlCarousel({
                items: 5,
                nav: true,
                dots: false,
                navText: ['<i class="fa fa-caret-left"></i>', '<i class="fa fa-caret-right"></i>']
                });
    });
    $(document).ready(function () {
                $(".partner-carousel").owlCarousel({
                    items: 5,
                    nav: true,
                    dots: false,
                    navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>']
                });
    });


    $(document).ready(function () {
                $('.slider-for').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                arrows: false,
                fade: true,
                centerMode: true,
                asNavFor: '.slider-nav'
                });
                $('.slider-nav').slick({
                slidesToShow: 3,
                slidesToScroll: 1,
                asNavFor: '.slider-for',
                dots: true,
                centerMode: true,
                focusOnSelect: true,
                variableWidth: true,
                adaptiveHeight: true,
                // vertical:true,
                });
    });


    $(document).ready(function () {
                var quantitiy = 0;
                $('.quantity-right-plus').click(function (e) {
                e.preventDefault();
                var quantity = parseInt($('#quantity').val());
                $('#quantity').val(quantity + 1);
                });
                $('.quantity-left-minus').click(function (e) {
                e.preventDefault();
                var quantity = parseInt($('#quantity').val());
                if (quantity > 0) {
                    $('#quantity').val(quantity - 1);
                }
                });
    });

    function formatted_url(r){
			var a={search:{},hash:{}},
				e=new URL(r);
			for(var s of Array(2).keys())
				for(var n=1==s?"hash":"search",h=e[n].substring(1).split("&"),t=0;t<h.length; t++){
					var o=h[t].split("=");
					o[0]&&(a[n][o[0]] = decodeURIComponent(o[1]))
				}
			return a
		}

    function url_to_string(obj) {
			var str = [];
			for(var p in obj)
				str.push(encodeURIComponent(p) + "=" + obj[p]);
			return `?${str.join("&")}`;
		}

//	$(".ial-filter__comp-title").click(function(e){
//	         e.preventDefault();
//            let contentEl = e.target.parentElement.children[1];
//            e.target.classList.toggle('ial-filter__comp-title--show');
//            contentEl.classList.toggle('d-none');
//
//	    });

    $(".attr-model-gst").click(function(){
			var attr_model_input = $(".attr-model-input-gst");
			var branch_ids = [];
			for (var i=0;i<attr_model_input.length;i++){
				if ($(attr_model_input[i]).prop("checked")){
					branch_ids.push($(attr_model_input[i]).attr("filter-data"))
				}
			}
			var branch_query = branch_ids.join("-");
			var url_query = formatted_url(location.href);
			if (branch_query){
				url_query.search.models = branch_query;
			}else{
				delete url_query.search.models;
			}
			var new_query = url_to_string(url_query.search);
			$.post("/get_gearstore_view", url_query.search, function( data ) {
				$("#product-view-list").html( data );
			});
			history.pushState(null, null, new_query);
		});

});


odoo.define('iwesabe_website_theme.best_seller', function (require) {
   $(document).ready(function () {
            $(".ia-carousel").owlCarousel({
                margin: 0,
                nav: true,
                dots: false,
                navText: ['<i class="fa fa-caret-left"></i>', '<i class="fa fa-caret-right"></i>'],
                responsive: {
                    480: {
                       items: 1
                   },
                }
            });
        });

})