import os
from django import template
from longclaw import settings

register = template.Library()

CLIENT_PATH = os.path.join('core', 'js', 'longclawclient.bundle.js')
VENDORS_PATH = os.path.join('core', 'js', 'vendors.bundle.js')

@register.inclusion_tag("core/script.html")
def longclaw_vendors_bundle():
    try:
        assert os.path.exists(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', VENDORS_PATH)
        )
    except AssertionError:
        raise AssertionError("The longclaw vendors bundle does not exist in staticfiles, have you run collectstatic? "
                             "Note: if this doesn't work, in longclaw/core/client run npm install npm run build."
                             "Then run python manage.py collectstatic.")
    return {'path': VENDORS_PATH}

@register.inclusion_tag("core/script.html")
def longclaw_client_bundle():
    try:
        assert os.path.exists(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', CLIENT_PATH)
        )
    except AssertionError:
        raise AssertionError("The longclaw vendors bundle does not exist in staticfiles, have you run collectstatic? "
                             "Note: if this doesn't work, in longclaw/core/client run npm install npm run build."
                             "Then run python manage.py collectstatic.")

    return {'path': CLIENT_PATH}

@register.simple_tag
def longclaw_api_url_prefix():
    return settings.API_URL_PREFIX


