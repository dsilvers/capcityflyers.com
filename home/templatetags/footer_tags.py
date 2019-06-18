from django import template

from home.models import FooterContent

register = template.Library()


@register.inclusion_tag('footer.html', takes_context=True)
def footer_content(context):
    footer = FooterContent.objects.first()

    if footer is None:
        footer = FooterContent()

    return {
        'footer': footer,
    }
