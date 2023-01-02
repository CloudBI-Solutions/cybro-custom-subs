//$(document).ready(function(){
//    console.log('gaming pc filter....')
//    let filteTitleEls = document.querySelectorAll('.ial-filter__comp-title');
//    console.log('filteTitleEls', filteTitleEls)
//    filteTitleEls.forEach(function (filteTitleEl) {
//        filteTitleEl.addEventListener('click', function (e) {
//            console.log('filteTitleEl.addEventListener')
//            e.preventDefault();
//            let contentEl = e.target.parentElement.children[1];
//            e.target.classList.toggle('ial-filter__comp-title--show');
//            contentEl.classList.toggle('d-none');
//        });
//    });
//
//    let mobIconEl = document.querySelector('.ial-filter__mob-icon');
//    let mobFilterEl = document.querySelector('.ial-filter-container');
//    let mobCloseIconEl = document.querySelector('.ial-filter-container__close');
//    mobIconEl.addEventListener('click', function (e) {
//        e.preventDefault();
//        mobFilterEl.classList.remove('ial-filter-container--resp-hide')
//    })
//    mobCloseIconEl.addEventListener('click', function (e) {
//        e.preventDefault();
//        mobFilterEl.classList.add('ial-filter-container--resp-hide')
//    });
//});

$(document).ready(function () {
        $('.ian-home__product-slider').slick({
          infinite: true,
          slidesToShow: 4,
          slidesToScroll: 4,
          arrows: false,
          slickPlay: true,
          prevArrow: "<svg class='ia-carousel__beta-nav ia-carousel__beta-nav--prev' width='46' height='46' fill='none' stroke='#ffffff' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'> <path d='m15.5 18-6-6 6-6'></path></svg>",
          nextArrow: "<svg class='ia-carousel__beta-nav ia-carousel__beta-nav--next' width='46' height='46' fill='none' stroke='#ffffff' stroke-width='1.5' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path d='m9.5 6 6 6-6 6'></path></svg>",
          responsive: [
            {
              breakpoint: 1200,
              settings: {
                slidesToShow: 3,
                slidesToScroll: 3,
                infinite: true,
                dots: true
              }
            },
            {
              breakpoint: 800,
              settings: {
                slidesToShow: 2,
                slidesToScroll: 2
              }
            },
            {
              breakpoint: 520,
              settings: {
                slidesToShow: 1,
                slidesToScroll: 1
              }
            }
          ]
        });
      });


//$(document).ready(function () {
//      $('.ian-home__slider-beta').slick({
//        infinite: true,
//        slidesToShow: 3,
//        slidesToScroll: 3,
//        arrows: true,
//        prevArrow: "<svg class='ia-carousel__beta-nav ia-carousel__beta-nav--prev' width='46' height='46' fill='none' stroke='#ffffff' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'> <path d='m15.5 18-6-6 6-6'></path></svg>",
//        nextArrow: "<svg class='ia-carousel__beta-nav ia-carousel__beta-nav--next' width='46' height='46' fill='none' stroke='#ffffff' stroke-width='1.5' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path d='m9.5 6 6 6-6 6'></path></svg>",
//        responsive: [
//          {
//            breakpoint: 1024,
//            settings: {
//              slidesToShow: 3,
//              slidesToScroll: 3,
//              infinite: true,
//              dots: true
//            }
//          },
//          {
//            breakpoint: 600,
//            settings: {
//              slidesToShow: 2,
//              slidesToScroll: 2
//            }
//          },
//          {
//            breakpoint: 480,
//            settings: {
//              slidesToShow: 1,
//              slidesToScroll: 1
//            }
//          }
//        ]
//      });
//    });


$(document).on("click", "#o_logout", function() {
     var close_popup= $("#otp_login")
     console.log('mhjkjfjfjjfjfj')
     window.location.href = "/web/session/logout?redirect=/";
    });

$(document).ready(function () {
        $(".ia-secondary-carousel").owlCarousel({
            items: 3,
            stageClass: 'ia-carousel-stage',
            nav: false,
            navText: ["<img  class='ia-secondary-nav-icons' src='iwesabe_website_theme/static/src/img/right-arrow 2.png' />", "<img class='ia-secondary-nav-icons' src='iwesabe_website_theme/static/src/img/right-arrow 1.png' />"],
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,
                    nav: true
                },
                600: {
                    items: 2,
                    nav: false
                },
                1000: {
                    items: 3,
                    nav: true,
                    loop: false
                }
            }
        });
    });


$(document).on('click', '#go_back', function(){

    window.history.back();
     console.log("test")
 });

$(document).ready(function() {

	$("#accordion li > h4").click(function () {

		if ($(this).next().is(':visible')) {
			$(this).next().slideUp(300);
			$(this).children(".plusminus").addClass('fa-caret-down');
			$(this).children(".plusminus").removeClass('fa-caret-up');
		} else {
			$(this).next("#accordion ul").slideDown(300);
			$(this).children(".plusminus").addClass('fa-caret-up');
			$(this).children(".plusminus").removeClass('fa-caret-down');
		}
	});
	
// Car View Set Fixed Right side
	var div = $("#floater");
	$('#wrapwrap').scroll(function() {
		if($(this).scrollTop() > 1000){
			div.addClass("fixed_top_cart");
		}else{
			div.removeClass("fixed_top_cart");
		}
		
	});
	
	window.myFunction = function(event) {
		// reset all menu items
		console.log("Allll -->>>")
		document.querySelectorAll('ul li.active').forEach(function(item) {
			item.classList.remove('active');
		})
			// mark as active selected menu item
			event.target.classList.add("active");
			console.log("event.",event)
		};


	
});
