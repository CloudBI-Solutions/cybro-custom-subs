from odoo import models,fields
from PIL import ImageColor
class itemInherit(models.Model):
    _inherit="ks_dashboard_ninja.item"

    def get_style_main_body_layout_1(self,item):
        background = list(ImageColor.getcolor(item.ks_background_color.split(',')[0], "RGB"))
        background_a = item.ks_background_color.split(',')[1]
        font_a = item.ks_font_color.split(',')[1]
        font = list(ImageColor.getcolor(item.ks_font_color.split(',')[0], "RGB"))
        background.append(float(background_a))
        font.append(float(font_a))
        return "background-color:" + "rgba"+str(tuple(background)) + ";color : " +"rgba"+ str(tuple(font)) + ";"

    def get_ks_rgba_default_icon_color_layout_1(self,item):
        icon_color = list(ImageColor.getcolor(item.ks_default_icon_color.split(',')[0], "RGB"))
        icon_color_a = item.ks_default_icon_color.split(',')[1]
        icon_color.append(float(icon_color_a))
        return "rgba"+str(tuple(icon_color))

    # def get_ks_icon_url_layout_1(self,item):
    #     print(item)
    #     icon = item.ks_icon
    #     print(icon,'icccccccccccccccccccc')

    def get_ks_record_count(self,item):
        count = round(item.ks_record_count)
        return count

    def get_style_image_body_l2(self,item):
        background = list(ImageColor.getcolor(item.ks_background_color.split(',')[0], "RGB"))
        new_bg = []
        for item_back in background:
            new_bg.append(item_back-25)

        background_a = item.ks_background_color.split(',')[1]
        new_bg.append(float(background_a))
        return "background-color:" +  "rgba"+str(tuple(new_bg)) + ";"

    def get_style_image_body_l2_layout_4(self, item):
        background = list(ImageColor.getcolor(item.ks_background_color.split(',')[0], "RGB"))
        background_a = item.ks_background_color.split(',')[1]
        background.append(float(background_a))
        return "background-color:" +  "rgba"+str(tuple(background)) + ";"


    def get_style_domain_count_body(self,item):
        background = list(ImageColor.getcolor(item.ks_background_color.split(',')[0], "RGB"))
        background_a = item.ks_background_color.split(',')[1]
        background.append(float(background_a))
        return "color:" + "rgba" + str(tuple(background)) + ";"

    def get_ks_icon_url(self,item):
        img = item.ks_icon
        img_new = str(img).split("'")
        return 'data:image/png' + ';base64,' + img_new[1];
