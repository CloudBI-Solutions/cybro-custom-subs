odoo.define('badminto.website_video_widget', function (require) {
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


    var BadmintoVideoPreview = BasicFields.FieldBinaryImage.extend( {
        template: 'BadmintoVideoPreview',
        events: _.extend({}, BasicFields.FieldBinaryImage.prototype.events, {
            'click .o_file_upload_button': '_on_file_upload_button',
            'click .o_play_video_button': '_on_play_video_button',
            'click .o_select_new_video_button': '_on_select_new_video_button',
            'click .o_clear_video_button': '_on_clear_video_button',
            'click .o_download_video_button': '_on_Download_Click',
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
                           model: 'badminto.assessment',
                           method: 'upload_video_badminto',
                           args: [,res_id,base64String,filename,self.attrs.name],
                           });
                        state='';
                    }else if(state=='delete'){
                        self.$el.find('.o_download_video_button_edit_view').css('display','none');
                        rpc.query({
                            model: 'badminto.assessment',
                            method: 'update_video_badminto',
                            args: [,res_id,self.attrs.name],
                            });
                        state='';
                    }
                    rpc.query({
                        model: 'badminto.assessment',
                        method: 'load_video_badminto',
                        args: [,res_id, self.attrs.name],
                    }).then(function (result) {
                        if(result){
                            if(result['datas'] && result['name']){
                                $("<video class='img img-fluid' src='"+result['datas']+"' controls='controls'></video>" ).insertAfter(self.$el.find('img') );
                                self.$el.find('img').css('display','none');
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
                        model: 'badminto.assessment',
                        method: 'load_video_badminto',
                        args: [,res_id,self.attrs.name],
                    }).then(function (result) {
                        if(result){
                            if(result['datas'] && result['name']){
                                $("<video class='img img-fluid' src='"+result['datas']+"' controls='controls'></video>" ).insertAfter(self.$el.find('img') );
                                self.$el.find('img').css('display','none');
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
            var res_id=self.res_id;
            var onFileSelected = function(e){
                var reader = new FileReader();
                reader.onloadend = () => {
                    base64String = reader.result;
                    filename=this.files[0].name;
                    state='upload';
                    rpc.query({
                           model: 'badminto.assessment',
                           method: 'upload_video_badminto',
                           args: [,res_id,base64String,filename,self.attrs.name],
                           });
                    self.$el.find(".o_input_file_name").val(this.files[0].name);
                    };
                const validImageTypes = ['video/mp4'];
                if (validImageTypes.includes(this.files[0].type)) {
                    reader.readAsDataURL(this.files[0]);
                    self.$el.find('img').css('display','none');
                    $("<video class='img img-fluid' src='"+URL.createObjectURL(this.files[0])+"' controls='controls'></video>" ).insertAfter(self.$el.find('img') );

                    self.$el.find(".o_file_upload_button").css('display','none');
                    self.$el.find(".o_play_video_button").css('display','block');
                    self.$el.find(".o_download_video_button").css('display','block');
                    self.$el.find(".o_clear_video_button").css('display','block');
                    self.$el.find(".o_select_new_video_button").css('display','block');
                    self.$el.find(".o_input_file_name").css('display','block');
                }else{
                    Dialog.alert(this, "Upload mp4 files only");
                    self.$el.find(".o_file_upload_button").css('display','block');
                    self.$el.find(".o_play_video_button").css('display','none');
                    self.$el.find(".o_download_video_button").css('display','none');
                    self.$el.find(".o_clear_video_button").css('display','none');
                    self.$el.find(".o_select_new_video_button").css('display','none');
                    self.$el.find(".o_input_file_name").css('display','none');
                }
            };
            var FileUpload = $('<input type="file">');
            FileUpload.click();
            FileUpload.on("change",onFileSelected);
        },

         //  FILE UPDATING
         _on_select_new_video_button: function () {
            var self=this;
            var res_id=self.res_id;
            var onFileSelected = function(e){
            var reader = new FileReader();
            reader.onloadend = () => {
                base64String = reader.result;
                rpc.query({
                   model: 'badminto.assessment',
                   method: 'upload_video_badminto',
                   args: [,res_id,base64String,this.files[0].name,self.attrs.name],
                   });
                self.$el.find(".o_input_file_name").val(this.files[0].name);
            };
            const validImageTypes = ['video/mp4'];
            if (validImageTypes.includes(this.files[0].type)) {
                state='update';
                reader.readAsDataURL(this.files[0]);
                self.$el.find('video').attr('src',URL.createObjectURL(this.files[0]))
                self.$el.find(".o_file_upload_button").css('display','none');
                self.$el.find(".o_play_video_button").css('display','block');
                self.$el.find(".o_download_video_button").css('display','block');
                self.$el.find(".o_clear_video_button").css('display','block');
                self.$el.find(".o_select_new_video_button").css('display','block');
                self.$el.find(".o_input_file_name").css('display','block');
            }else{
                Dialog.alert(this, "Upload mp4 files only");
                self.$el.find(".o_file_upload_button").css('display','block');
                self.$el.find(".o_play_video_button").css('display','none');
                self.$el.find(".o_download_video_button").css('display','none');
                self.$el.find(".o_clear_video_button").css('display','none');
                self.$el.find(".o_select_new_video_button").css('display','none');
                self.$el.find(".o_input_file_name").css('display','none');
            }
        };
        var FileUpload = $('<input type="file">');
        FileUpload.click();
        FileUpload.on("change",onFileSelected);
        },

        //  DELETING UPLOADED FILE

        _on_clear_video_button: function () {
        var self=this;
            state='delete';
            rpc.query({
                model: 'badminto.assessment',
                method: 'update_video_badminto',
                args: [,self.res_id,self.attrs.name],
                });
            self.$el.find('video').css('display', 'none');
            self.$el.find('img').css('display','block');

            self.$el.find(".o_input_file_name").val('');
            self.$el.find(".o_file_upload_button").css('display','block');
            self.$el.find(".o_play_video_button").css('display','none');
            self.$el.find(".o_clear_video_button").css('display','none');
            self.$el.find(".o_select_new_video_button").css('display','none');
            self.$el.find(".o_input_file_name").css('display','none');
            self.$el.find(".o_download_video_button").css('display','none');
        },

        //  PLAYING UPLOADED FILE
        _on_play_video_button: function () {
            var res_id=this.res_id;

//            ADD RPC QUERY TO GET THE VIDEO

            rpc.query({
                   model: 'badminto.assessment',
                   method: 'play_video_badminto',
                   args: [,res_id,this.attrs.name],
                   }).then(function (result) {
                      new Dialog(this, {$content: $('<htmlData><video controls autoplay style="width:100%;"><source type="video/mp4" src="'+result.datas+'"/></video></htmlData>')}).open();
             });
        },

    });
    Registry.add('video_widget', BadmintoVideoPreview);
});
