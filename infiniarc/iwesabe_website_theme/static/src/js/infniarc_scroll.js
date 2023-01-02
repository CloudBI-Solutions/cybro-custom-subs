odoo.define('iwesabe_website_theme.infniarc_scroll', function (require) {
'use strict';

	var publicWidget = require('web.public.widget');
	var animations = require('website.content.snippets.animation');

	const InfiniarcAnimation = animations.Animation.extend({
		disabledInEditableMode: false,
		effects: [{
			startEvents: 'scroll',
			update: '_updateHeaderOnScroll',
		}],
		
		init: function () {
			this._super(...arguments);
			var animation = false;
		},
		start: function () {
			this.$el.on('odoo-transitionstart.InfiniarcAnimation', () => this._adaptToHeaderChangeLoop(1));
			return this._super(...arguments);
		},
		_updateHeaderOnScroll:function(scroll){
			$(".component_list_part").each(function(i,e){
				var visible_ele = $(e).position().top - 200;
				if (scroll >= visible_ele){
					var visible_ele_id = $(e).attr("id");
					var target_ele = $(`.vertical-tabs > ul > li > a[href='#${visible_ele_id}']`);
					var target_active_ele = $(`.vertical-tabs > ul > li > a.active`);
					target_active_ele.removeClass("active");
					target_ele.addClass("active");
				}
			})
		}
	});

	publicWidget.registry.InfiniarBodyAnimation = InfiniarcAnimation.extend({
		selector: 'main',
	});
});









