# Generated by Django 2.2.2 on 2019-06-18 06:32

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('aircraft', '0003_auto_20190618_0629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraftpage',
            name='aircraft_images',
            field=wagtail.core.fields.StreamField([('carousel', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(blank=True, default='', max_length=120, null=True, required=False)), ('description', wagtail.core.blocks.RichTextBlock(blank=True, default='', null=True, required=False))], blank=True, null=True, required=False))], blank=True),
        ),
    ]
