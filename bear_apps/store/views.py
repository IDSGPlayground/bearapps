# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse

def home(request):
    # TODO Change this code to use render_to_response() to cut down on
    # boilerplate code when making basic views:
    # https://docs.djangoproject.com/en/dev/intro/tutorial03/#a-shortcut-render-to-response
    t = loader.get_template('index.html')
    c = Context()
    return HttpResponse(t.render(c))
