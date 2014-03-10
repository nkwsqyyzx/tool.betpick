from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse

from tool.OddsProvider import OddsProvider

def odds(request,mid):
    p = OddsProvider(mid)
    rs = p.getResult()
    tp = """
    <html>
    <head><title>Ordering notice</title></head>

    <body>

    <ul>
    {% for item in r.asian %}
        <li>{{ item.1 }}</li>
    {% endfor %}
    </ul>

    </body>
    </html>
    """

    t = Template(tp)
    rr = None
    for r in rs:
        rr = r
        break
    c = Context({'r': rr})

    return HttpResponse(t.render(c))

def home(request):
    t = get_template('home.html')
    html = t.render(Context())
    return HttpResponse(html)
