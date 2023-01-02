odoo.define('latest_blog_snippet.s_dynamic_snippet_blog', function(require){
    'use strict';
    var core = require('web.core');
    var sAnimation = require('website.content.snippets.animation');
    var _t = core._t;
    var ajax = require('web.ajax');
    console.log('Halooo')

    sAnimation.registry.latest_blogs = sAnimation.Class.extend({
        selector: '.s_blog_carousel',
        start: function(){
            this._super.apply(this, arguments);
            var self = this;
            ajax.jsonRpc('/latest_blog_snippet/blog_snippet', 'call', {})
            .then(function (data){
            console.log("haii", data)
                if(data){
                    self.$target.append(data);
                }
            });
        },
    });
});
