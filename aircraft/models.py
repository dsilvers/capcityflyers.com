from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.blocks import ImageChooserBlock


class AircraftImageBlock(blocks.StreamBlock):
    carousel = blocks.StructBlock([
        (('image'), ImageChooserBlock()),
        (('title'), blocks.CharBlock(max_length=120, blank=True, null=True, default='')),
        (('description'), blocks.RichTextBlock(blank=True, null=True, default='')),
    ])


class AircraftPage(Page):
    frontpage_blurb = models.CharField(max_length=255, blank=True)
    frontpage_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    aircraft_make_model = models.CharField(max_length=200)
    aircraft_tail_number = models.CharField(max_length=50)

    aircraft_description = RichTextField(blank=True)

    billing_wet_rate = models.CharField(max_length=200, blank=True)
    billing_dry_rate = models.CharField(max_length=200, blank=True)
    billing_last_updated = models.DateField(blank=True)

    pilot_requirements = RichTextField(blank=True)

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    aircraft_images = StreamField(AircraftImageBlock(), blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('aircraft_make_model'),
                FieldPanel('aircraft_tail_number'),
                FieldPanel('aircraft_description'),
            ],
            heading="Aircraft Details",
        ),

        MultiFieldPanel(
            [
                FieldPanel('frontpage_blurb'),
                ImageChooserPanel('frontpage_image'),
            ],
            heading="Frontpage Content",
        ),

        MultiFieldPanel(
            [
                FieldPanel('billing_wet_rate'),
                FieldPanel('billing_dry_rate'),
                FieldPanel('billing_last_updated'),
            ],
            heading="Billing Details",
        ),

        FieldPanel('pilot_requirements'),

        InlinePanel('documents', label="Documents"),

        ImageChooserPanel('header_image'),

        StreamFieldPanel('aircraft_images'),
    ]


class AircraftPageDocumentLink(Orderable):
    page = ParentalKey(AircraftPage, related_name='documents')
    document = models.ForeignKey(
        'wagtaildocs.Document', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        DocumentChooserPanel('document'),
    ]
