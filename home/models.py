from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image as WagtailImage
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

import os
from PIL import Image as PILImage

from aircraft.models import AircraftPage


class FooterContent(models.Model):
    footer_blurb_header = models.CharField(max_length=255)
    footer_blurb_text = RichTextField()

    youtube_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)

    contact_phone_number = models.CharField(max_length=255, blank=True)
    contact_address = models.CharField(max_length=255, blank=True)
    contact_address_map_link = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)

    copyright_text = models.CharField(max_length=255)

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('footer_blurb_header'),
                FieldPanel('footer_blurb_text', classname="full"),
            ],
            heading="Footer Content",
        ),
        MultiFieldPanel(
            [
                FieldPanel('contact_phone_number'),
                FieldPanel('contact_address'),
                FieldPanel('contact_address_map_link'),
                FieldPanel('contact_email'),
            ],
            heading="Footer Contact Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel('youtube_link'),
                FieldPanel('facebook_link'),
            ],
            heading="Footer Links",
        ),
        FieldPanel('copyright_text'),
    ]

    def __str__(self):
        return "Footer Content (Text, Contact Details, Links, Copyright)"


class HomePage(Page):
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    hero_heading = models.CharField(max_length=255, blank=True)
    hero_subheading = models.CharField(max_length=255, blank=True)

    home_heading = models.CharField(max_length=255, blank=True)
    home_content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_heading'),
                FieldPanel('hero_subheading'),
            ],
            heading="Hero Image and Content",
        ),

        MultiFieldPanel(
            [
                FieldPanel('home_heading'),
                FieldPanel('home_content'),
            ],
            heading="Homepage Content",
        ),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['aircraft_pages'] = self.get_children().type(AircraftPage)
        return context


class MembershipPage(Page):
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    hero_heading = models.CharField(max_length=255, blank=True)
    hero_subheading = models.CharField(max_length=255, blank=True)

    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_heading'),
                FieldPanel('hero_subheading'),
            ],
            heading="Hero Image and Heading",
        ),
        FieldPanel('content'),
    ]


def get_image_render_full_path(file_path, render_name):
    original_filename, original_extension = os.path.splitext(os.path.basename(file_path))
    return '{}/images/{}.{}{}'.format(
        settings.MEDIA_ROOT,
        original_filename,
        render_name,
        original_extension
    )


@receiver(post_save, sender=WagtailImage)
def WagtailImageGenerateImageSizes(sender, instance, **kwargs):
    original_file = settings.MEDIA_ROOT + '/' + instance.file.path
    im = PILImage.open(instance.file.path)
    original_width, original_height = im.size

    for render_name, new_width in settings.RENDER_IMAGE_SIZES.items():
        new_height = int(new_width * original_height / original_width)
        im_resized = im.resize((new_width, new_height), PILImage.ANTIALIAS)
        im_resized.save(get_image_render_full_path(instance.file.path, render_name), quality=86)


@receiver(pre_delete, sender=WagtailImage)
def WagtailImageDeleteImageSizesCleanup(sender, instance, **kwargs):
    for render_name in settings.RENDER_IMAGE_SIZES:
        image_path = get_image_render_full_path(instance.file.path, render_name)
        if os.path.exists(image_path):
            os.remove(image_path)
