odoo.define('theme_sport_erp.header',function(require){
    "use strict";

    $(document).ready(function () {
        $('.video').click(function () { this.paused ? this.play() : this.pause(); });

       $('#mobileMenuToggler, #mobileMenuClose').on('click', function (e) {
       $('#mobileMenu').toggleClass('d-none');
        })
        // What's Included Toggle
        let whatsIncludedEl =
        document.querySelectorAll('.set-pricing-card__whats-included');

        whatsIncludedEl.forEach(el => {
        el.addEventListener('click', function (e) {
        e.preventDefault();
        let targetEl = e.target.dataset.target;
        let targetDOM = document.querySelector(`#${targetEl}`);
        if (targetDOM) {
            targetDOM.classList.toggle('d-none');
        }
        });
        });

        let generalAccordionEls =
            document.querySelectorAll('.set-accordion__header');

            generalAccordionEls.forEach(accordion => {
            accordion.addEventListener('click', function (e) {
            e.preventDefault();
            if
            (e.target.parentElement.children[1].classList.contains('set-accordion__body'))
            {
            e.target.parentElement.children[1].classList.toggle('d-none');
            e.target.parentElement.children[0].children[1].classList.toggle('set-accordion__sign--plus');
            } else {
            e.target.parentElement.parentElement.children[1].classList.toggle('d-none');
            e.target.parentElement.parentElement.children[0].children[1].classList.toggle('set-accordion__sign--plus');
            }
            });
            });
    });
});
