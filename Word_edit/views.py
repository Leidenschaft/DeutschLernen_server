from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader

from .html_form_to_xml import parsegen, savedit

def create_response(request):
    """
    response for "Word_edit/create_new_word",GET to create new word, POST to update old word
    """
    rq = request.POST
    if rq:
        reqsheet, err, err_str = parsegen(rq)
        if err != 0:
            return HttpResponseBadRequest(err_str)
        savedit(reqsheet)
        return HttpResponse('All right, click <a href="http://'
                            + request.get_host() + request.get_full_path()
                            + '">create another</a>')
    # GET Method here
    context = {}
    context['wordAddrchoice'] = 'None'
    context['isCreated'] = 'True'
    template = loader.get_template('Word_edit/editing_interface.html')
    return HttpResponse(template.render(context, request))
