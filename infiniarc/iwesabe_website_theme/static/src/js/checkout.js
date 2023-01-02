odoo.define('iwesabe_website_theme.checkout', function (require) {
 function cc_format(value) {
            var v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '')
            var matches = v.match(/\d{4,16}/g);
            var match = matches && matches[0] || ''
            var parts = []
            for (i = 0, len = match.length; i < len; i += 4) {
                parts.push(match.substring(i, i + 4))
            }
            if (parts.length) {
                return parts.join('  ')
            } else {
                return value
            }
        }
          window.onload = function () {
            document.getElementById('creditCard').oninput = function () {
                this.value = cc_format(this.value)
            }
        }
         let locationRadioEl = document.querySelectorAll('.ia-checkout__local-location-radio');

        // Check on loading the document
        locationRadioEl.forEach(item => {
            if (item.checked) {
                item.parentElement.classList.add('ia-checkout__local-location--active');
            } else {
                item.parentElement.classList.remove('ia-checkout__local-location--active');
            }
        });
        // Check on selecting an option
        let locationEl = document.querySelectorAll('.ia-checkout__local-location');
        locationEl.forEach(item => {
            item.addEventListener('click', event => {
                // Remove existing selections
                locationRadioEl.forEach(item => {
                    item.parentElement.classList.remove('ia-checkout__local-location--active');
                })
                 // Check if we're clicking on the parent element and active class already exists
                if (event.target.classList.contains('ia-checkout__local-location') && !event.target.classList.contains('ia-checkout__local-location--active')) {
                    event.target.classList.add('ia-checkout__local-location--active');
                } else if (!event.target.classList.contains('ia-checkout__local-location')) {
                    // If not, then add the active class to the parent element.
                    event.target.parentElement.classList.add('ia-checkout__local-location--active');
                }
            })
        })
         let discountInput = document.querySelector('#discountCodeInput');
        let discountBtn = document.querySelector('#discountBtn');
//
//        discountBtn.addEventListener('click', function(e){
//            e.preventDefault();
//
//            if(discountInput.classList.contains('d-none')){
//                discountInput.classList.remove('d-none');
//            }
//        })
})