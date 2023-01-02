odoo.define('badminto.remove_video', function (require) {
    "use strict";
    var publicWidget = require('web.public.widget');

    publicWidget.registry.RemoveVideo = publicWidget.Widget.extend({
        selector: '.badminto-video--modals',
        events: {
            'click .remove--video--badminto': '_onRemoveVideoClicked',
            'change .badminto-video-input': '_onFileChanged',
            },
             _onRemoveVideoClicked: function (ev) {
             console.log('this', this.$el.find('video')[0]);
             this.$el.find('video')[0].src='';
             this.$el.find('video')[0].style.display = "none";
             this.$el.find('input')[0].value = null;
            },
            _onFileChanged: function (ev) {
            console.log("haii")
            this.$el.find('video')[0].style.display = "block";
            this.$el.find('video')[0].src=URL.createObjectURL(event.target.files[0]);


            },
        });

    });