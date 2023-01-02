odoo.define('website_video_adds.website_video_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var BasicFields= require('web.basic_fields');
    var Registry = require('web.field_registry');
    var rpc = require('web.rpc');
    var Dialog = require('web.Dialog');
    var _t = core._t;
    var QWeb = core.qweb;
    var res_id;
    var base64String = 'False';
    var filename;
    var state;


    var FieldWebVideo = BasicFields.FieldBinaryImage.extend( {
        template: 'FieldWebVideo',
        events: _.extend({}, BasicFields.FieldBinaryImage.prototype.events, {
            'click .o_file_upload_button': '_on_file_upload_button',
            'click .o_play_video_button': '_on_play_video_button',
            'click .o_select_new_video_button': '_on_select_new_video_button',
            'click .o_clear_video_button': '_on_clear_video_button'
        }),


        //  START FUNCTION

        start: function () {
            var self=this;
            return this._super().then(function(){
                self.$el.find('img[name="web_video_file"]').css('display','none');
                self.$el.find('.o_file_upload_button').css('display','none');
                res_id=self.res_id;
                if (self.mode=='readonly'){
                    if (state=='upload'){
                        self.$el.find('.o_download_video_button_edit_view').css('display','block');
                        rpc.query({
                           model: 'product.template',
                           method: 'upload_video_adds',
                           args: [,res_id,base64String,filename],
                           });
                        state='';
                    }else if(state=='delete'){
                        self.$el.find('.o_download_video_button_edit_view').css('display','none');
                        rpc.query({
                            model: 'product.template',
                            method: 'update_video_adds',
                            args: [,res_id],
                            });
                        state='';
                    }
                    rpc.query({
                        model: 'product.template',
                        method: 'load_video_adds',
                        args: [,res_id],
                    }).then(function (result) {
                        if(result){
                            if(result['datas'] && result['name']){
                                self.$el.find('.o_play_video_button').css('display','none');
                                self.$el.find('.o_download_video_button').css('display','none');
                                self.$el.find('.o_download_video_button_edit_view').css('display','block');
                                self.$el.find('.o_clear_video_button').css('display','none');
                                self.$el.find('.o_select_new_video_button').css('display','none');
                                self.$el.find('.o_input_file_name').css('display','none');
                                self.$el.find('.o_input_file_name').val(result['name']);
                                base64String=result['datas'];
                            }
                            else{
                                self.$el.find('.o_file_upload_button').css('display','none');
                                self.$el.find('.o_download_video_button_edit_view').css('display','none');
                                self.$el.find('.o_play_video_button').css('display','none');
                                self.$el.find('.o_download_video_button').css('display','none');
                                self.$el.find('.o_clear_video_button').css('display','none');
                                self.$el.find('.o_select_new_video_button').css('display','none');
                                self.$el.find('.o_input_file_name').css('display','none');
                                self.$el.find('.o_input_file_name').val('');
                                base64String='';
                            }
                        }else{
                            self.$el.find('.o_file_upload_button').css('display','none');
                            self.$el.find('.o_download_video_button_edit_view').css('display','none');
                            self.$el.find('.o_play_video_button').css('display','none');
                            self.$el.find('.o_download_video_button').css('display','none');
                            self.$el.find('.o_clear_video_button').css('display','none');
                            self.$el.find('.o_select_new_video_button').css('display','none');
                            self.$el.find('.o_input_file_name').css('display','none');
                            self.$el.find('.o_input_file_name').val('');
                            base64String='';
                        }
                    });
                }else if (self.mode=='edit'){
                    rpc.query({
                        model: 'product.template',
                        method: 'load_video_adds',
                        args: [,res_id],
                    }).then(function (result) {
                        if(result){
                            if(result['datas'] && result['name']){
                                self.$el.find('.o_play_video_button').css('display','block');
                                self.$el.find('.o_download_video_button').css('display','block');
                                self.$el.find('.o_download_video_button_edit_view').css('display','none');
                                self.$el.find('.o_clear_video_button').css('display','block');
                                self.$el.find('.o_select_new_video_button').css('display','block');
                                self.$el.find('.o_input_file_name').css('display','block');
                                self.$el.find('.o_input_file_name').val(result['name']);
                                base64String=result['datas'];
                            }
                            else{
                                self.$el.find('.o_file_upload_button').css('display','block');
                                self.$el.find('.o_download_video_button_edit_view').css('display','none');
                                self.$el.find('.o_play_video_button').css('display','none');
                                self.$el.find('.o_download_video_button').css('display','none');
                                self.$el.find('.o_clear_video_button').css('display','none');
                                self.$el.find('.o_select_new_video_button').css('display','none');
                                self.$el.find('.o_input_file_name').css('display','none');
                                self.$el.find('.o_input_file_name').val('');
                                base64String='';
                            }
                        }else{
                            self.$el.find('.o_file_upload_button').css('display','block');
                            self.$el.find('.o_download_video_button_edit_view').css('display','none');
                            self.$el.find('.o_play_video_button').css('display','none');
                            self.$el.find('.o_download_video_button').css('display','none');
                            self.$el.find('.o_clear_video_button').css('display','none');
                            self.$el.find('.o_select_new_video_button').css('display','none');
                            self.$el.find('.o_input_file_name').css('display','none');
                            self.$el.find('.o_input_file_name').val('');
                            base64String='';
                        }
                    });
                }
            });
        },

        //  FILE UPLOADING
        _on_file_upload_button: function () {
            var self=this;
            var onFileSelected = function(e){
                var reader = new FileReader();



                reader.onloadend = () => {
                    base64String = reader.result;
                    filename=this.files[0].name;
                    state='upload';
                    $(".o_input_file_name").val(this.files[0].name);
                    $(".o_download_video_button").attr('href','/web/content/${attachmentId}?download=true');
                    };



                const validImageTypes = ['video/mp4'];
                if (validImageTypes.includes(this.files[0].type)) {


                    reader.readAsDataURL(this.files[0]);
                    $(".o_file_upload_button").css('display','none');
                    $(".o_play_video_button").css('display','block');
                    $(".o_download_video_button").css('display','block');
                    $(".o_clear_video_button").css('display','block');
                    $(".o_select_new_video_button").css('display','block');
                    $(".o_input_file_name").css('display','block');
                }else{
                    Dialog.alert(this, "Upload xlsx files only");
                    $(".o_file_upload_button").css('display','block');
                    $(".o_play_video_button").css('display','none');
                    $(".o_download_video_button").css('display','none');
                    $(".o_clear_video_button").css('display','none');
                    $(".o_select_new_video_button").css('display','none');
                    $(".o_input_file_name").css('display','none');
                }
            };
            var FileUpload = $('<input type="file">');
            FileUpload.click();
            FileUpload.on("change",onFileSelected);
        },

         //  FILE UPDATING
         _on_select_new_video_button: function () {
                 var onFileSelected = function(e){
            var reader = new FileReader();
            reader.onloadend = () => {
                base64String = reader.result;
                rpc.query({
                   model: 'product.template',
                   method: 'upload_video_adds',
                   args: [,res_id,base64String,this.files[0].name],
                   });
                $(".o_input_file_name").val(this.files[0].name);
                $(".o_download_video_button").attr('href',this.files);
            };
            const validImageTypes = ['video/mp4'];
            if (validImageTypes.includes(this.files[0].type)) {
                state=update;
                reader.readAsDataURL(this.files[0]);
                $(".o_file_upload_button").css('display','none');
                $(".o_play_video_button").css('display','block');
                $(".o_download_video_button").css('display','block');
                $(".o_clear_video_button").css('display','block');
                $(".o_select_new_video_button").css('display','block');
                $(".o_input_file_name").css('display','block');
            }else{
                Dialog.alert(this, "Upload xlsx files only");
                $(".o_file_upload_button").css('display','block');
                $(".o_play_video_button").css('display','none');
                $(".o_download_video_button").css('display','none');
                $(".o_clear_video_button").css('display','none');
                $(".o_select_new_video_button").css('display','none');
                $(".o_input_file_name").css('display','none');
            }
        };
        var FileUpload = $('<input type="file">');
        FileUpload.click();
        FileUpload.on("change",onFileSelected);
        },



        //  DELETING UPLOADED FILE
        _on_clear_video_button: function () {
            state='delete';
            $(".o_input_file_name").val('');
            $(".o_file_upload_button").css('display','block');
            $(".o_play_video_button").css('display','none');
            $(".o_clear_video_button").css('display','none');
            $(".o_select_new_video_button").css('display','none');
            $(".o_input_file_name").css('display','none');
            $(".o_download_video_button").css('display','none');
        },


        //  PLAYING UPLOADED FILE
        _on_play_video_button: function () {
           new Dialog(this, {$content: $('<htmlData><video controls autoplay style="width:100%;"><source type="video/mp4" src="'+base64String+'"/></video></htmlData>')}).open();
        },

    });
    Registry.add('video_widget', FieldWebVideo);
});
