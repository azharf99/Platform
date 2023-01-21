from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
# from io import StringIO
# from django.template import Context
# from cgi import parse
import pdfkit

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        print(sUrl, sRoot,mUrl, mRoot)
        print()

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
            print(path)
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
            print(path)
        else:
            print(uri)
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def render_to_pdf(template_src, context_dict, ekskul, bulan):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="laporan_{}_{}.pdf"'.format(ekskul, bulan)
    template = get_template(template_src)
    html = template.render(context_dict)

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisa_status.err:
        return HttpResponse("We had some error <pre>" + html + "</pre>")
    else:
        return response


    # template = get_template(template_src)
    # context = Context(context_dict)
    # html = template.render(context)
    # result = StringIO()
    #
    # pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result)
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return HttpResponse('We had some errors<pre>%s</pre>' % parse(html))



def render_ke_pdf(url, nama):
    return pdfkit.from_url(url, nama)