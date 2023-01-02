odoo.define('paceflow.videoPreview',function(require){
    "use strict";
    const { Component } = owl;
    const { useState } = owl.hooks;
    var openCVReady = 0;
    var FormRenderer = require('web.FormRenderer');
    var rpc = require("web.rpc");
    var document_id = 0;
    const { ComponentWrapper } = require('web.OwlCompatibility');

    class VideoPreviewComponent extends Component{
//        Need to fetch video from db to and need to return to the qweb from here.
//        Button clicking function
        phaseOneButton(ev){
            var button_id = ev.target.id;
            var button_name = ev.target.name;
            let video = document.getElementById("video_viewer"+button_id);
            video.pause();
            var capture = $('#capture'+button_id)[0];
            var snapshot = $('#snapshot')[0];
            var ctx = capture.getContext( '2d' );
            var img = new Image();
            var video_width= video.videoWidth;
            var video_height= video.videoHeight;
            if (video_height > video_width){
                video_height =video.videoHeight * 2;
                video_width= video.videoWidth *2 ;
                capture.width = video_width;
                capture.height = video_height;
            }
            else if(video_width < 1000){
                video_height =video.videoHeight * 2;
                video_width= video.videoWidth *2 ;
                capture.width = video_width;
                capture.height = video_height;
            }

            ctx.drawImage( video, 0, 0, video_width, video_height );
            img.src   = capture.toDataURL( "image/png" );
            img.id = 'image_element';
            ctx.drawImage( img, 0, 0, video_width, video_height );
            var data = {
                'image': img.src,
                'document_id': document_id,
                'button_name': button_name,
            };
            rpc.query({
                 model: "assessment.assessment",
                 method: "set_record_img",
                 args: [document_id,data],
             }).then(data => {
                 });


        }

    };
    Object.assign(VideoPreviewComponent,{
        template : "video_preview_widget"
    });
    FormRenderer.include({
        async _render(){
            await this._super(...arguments);
            for (const element of this.el.querySelectorAll('.o_video_preview_widget')) {
//          getting the data using Rpc
            document_id = this.state.res_id;
             this._rpc({
                 model: "assessment.assessment",
                 method: "get_current_record",
                 args: [[this.state.res_id]]
             }).then(data => {
                (new ComponentWrapper(this,VideoPreviewComponent,data))
                .mount(element)
                });
                }
            }
        });
});