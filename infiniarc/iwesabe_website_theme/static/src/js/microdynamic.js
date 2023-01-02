odoo.define('iwesabe_website_theme.microdynamic', function (require) {

	var ajax = require('web.ajax');
	console.log('loading...wwwwwwwwwwwwwww...............')

    $('.owl-carousel1').owlCarousel({
            loop: true,
            margin: 10,
            nav: true,
            autoWidth: true,
            dots: false,
            navText: ['<div class="pre"><i class="fas fa-caret-left"></i></div>', '<div class="nxt"><i class="fas fa-caret-right"></i></div>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 3
                },
                1000: {
                    items: 4
                }
            }
        })

        $(document).ready(function () {
      $('.ian-home__slider-beta').slick({
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 4,
        arrows: true,
        prevArrow: "<svg class='ia-carousel__beta-nav ia-carousel__beta-nav--prev' width='46' height='46' fill='none' stroke='#ffffff' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'> <path d='m15.5 18-6-6 6-6'></path></svg>",
        nextArrow: "<svg class='ia-carousel__beta-nav ia-carousel__beta-nav--next' width='46' height='46' fill='none' stroke='#ffffff' stroke-width='1.5' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path d='m9.5 6 6 6-6 6'></path></svg>",
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 3,
              infinite: true,
              dots: true
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2
            }
          },
          {
            breakpoint: 480,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1
            }
          }
        ]
      });
    });

    $(document).ready(function () {
      $('.ian-home__slider-explore-beta').slick({
        infinite: true,
        slidesToShow: 2,
        slidesToScroll: 2,
        arrows: true,
        slickPlay: true,
        prevArrow: "<svg class='ia-carousel__beta-nav ia-carousel__beta-nav--prev' width='46' height='46' fill='none' stroke='#ffffff' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'> <path d='m15.5 18-6-6 6-6'></path></svg>",
        nextArrow: "<svg class='ia-carousel__beta-nav ia-carousel__beta-nav--next' width='46' height='46' fill='none' stroke='#ffffff' stroke-width='1.5' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path d='m9.5 6 6 6-6 6'></path></svg>",
        responsive: [
          {
            breakpoint: 1200,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2,
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

    $(document).ready(function () {
            $(".owl-theme2").owlCarousel(
                {
                    items: 3,
                    loop: false,
                    margin: 40,
                    stagePadding: 0,
                    smartSpeed: 450,
                    autoplay: false,
                    autoPlaySpeed: 3000,
                    autoPlayTimeout: 1000,
                    autoplayHoverPause: true,
                    autoWidth: true,
                    dots: false,
                    nav: true,
                    navText: ['<div class="pre"><i class="fas fa-caret-left"></i></div>', '<div class="nxt"><i class="fas fa-caret-right"></i></div>'],
                    responsive: {
                        0: {
                            items: 1,
                        },
                        600: {
                            items: 2,
                        },
                        1000: {
                            items: 3,
                        }
                    }
                }
            );
        });

});
