from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from .models import FooterContent


class FooterContentAdmin(ModelAdmin):
    model = FooterContent


class BakeryModelAdminGroup(ModelAdminGroup):
    menu_label = 'CCF Misc'
    menu_icon = 'fa-cutlery'  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (FooterContentAdmin, )


modeladmin_register(BakeryModelAdminGroup)
