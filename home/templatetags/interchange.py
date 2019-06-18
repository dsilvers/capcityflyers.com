import os

from django.conf import settings

from django import template
register = template.Library()

"""
https://shermandigital.com/blog/tips-for-using-foundations-interchange/

<img alt="Profile" d
ata-interchange="

[/img/profile.jpg, (default)], 
[, (small)], 
[/img/profile-medium.jpg, (medium)], 
[/img/profile-large.jpg, (large)]


Foundation.Interchange.SPECIAL_QUERIES['smallretina'] = 'only screen and (min-width: 1px) and (-webkit-min-device-pixel-ratio: 2), only screen and (min-width: 1px) and (min--moz-device-pixel-ratio: 2), only screen and (min-width: 1px) and (-o-min-device-pixel-ratio: 2/1), only screen and (min-width: 1px) and (min-device-pixel-ratio: 2), only screen and (min-width: 1px) and (min-resolution: 192dpi), only screen and (min-width: 1px) and (min-resolution: 2dppx)';
Foundation.Interchange.SPECIAL_QUERIES['mediumretina'] = 'only screen and (min-width: 641px) and (-webkit-min-device-pixel-ratio: 2), only screen and (min-width: 641px) and (min--moz-device-pixel-ratio: 2), only screen and (min-width: 641px) and (-o-min-device-pixel-ratio: 2/1), only screen and (min-width: 641px) and (min-device-pixel-ratio: 2), only screen and (min-width: 641px) and (min-resolution: 192dpi), only screen and (min-width: 641px) and (min-resolution: 2dppx)';
Foundation.Interchange.SPECIAL_QUERIES['largeretina'] = 'only screen and (min-width: 1025px) and (-webkit-min-device-pixel-ratio: 2), only screen and (min-width: 1025px) and (min--moz-device-pixel-ratio: 2), only screen and (min-width: 1025px) and (-o-min-device-pixel-ratio: 2/1), only screen and (min-width: 1025px) and (min-device-pixel-ratio: 2), only screen and (min-width: 1025px) and (min-resolution: 192dpi), only screen and (min-width: 1025px) and (min-resolution: 2dppx)';
Foundation.Interchange.SPECIAL_QUERIES['xlargeretina'] = 'only screen and (min-width: 1921px) and (-webkit-min-device-pixel-ratio: 2), only screen and (min-width: 1921px) and (min--moz-device-pixel-ratio: 2), only screen and (min-width: 1921px) and (-o-min-device-pixel-ratio: 2/1), only screen and (min-width: 1921px) and (min-device-pixel-ratio: 2), only screen and (min-width: 1921px) and (min-resolution: 192dpi), only screen and (min-width: 1921px) and (min-resolution: 2dppx)';


" />
"""


def get_image_render_full_url(full_filename, render_name):
    filename, extension = os.path.splitext(os.path.basename(full_filename))
    return '{}images/{}.{}{}'.format(
        settings.MEDIA_URL,
        filename,
        render_name,
        extension
    )


def interchange(image_filename):
    interchange_urls = []
    interchange_urls.append(get_image_render_full_url(image_filename, 'original') + ", (default)")

    for name, width in settings.RENDER_IMAGE_SIZES.items():
        interchange_urls.append(
            "{}, {}".format(get_image_render_full_url(image_filename, name), name)
        )

    interchange_tag = "[" + "],[".join(interchange_urls) + "]"

    return {
        'tag': interchange_tag,
    }


@register.inclusion_tag('interchange_img.html')
def interchange_image(image_filename, **kwargs):
    return interchange(image_filename)


@register.inclusion_tag('interchange_div.html')
def interchange_div(image_filename, **kwargs):
    return interchange(image_filename)


@register.inclusion_tag('interchange_div.html')
def interchange_tag(image_filename, **kwargs):
    return interchange(image_filename)


@register.simple_tag
def interchange_original(image_filename):
    return get_image_render_full_url(image_filename, 'original')
