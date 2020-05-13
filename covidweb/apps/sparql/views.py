import urllib
import logging
import requests

from covidweb.apps.sparql.forms import SparqlForm
from django.shortcuts import render 
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse


logger = logging.getLogger(__name__)

HTTP_PROT = 'http://'
VIRTUOSO_HOST = getattr(settings, 'VIRTUOSO_HOST')
VIRTUOSO_SPARQL_PORT = getattr(settings, 'VIRTUOSO_SPARQL_PORT')
SPARQL_ENDPOINT_URL = HTTP_PROT + VIRTUOSO_HOST + ":" + str(VIRTUOSO_SPARQL_PORT) + "/sparql"


def sparql_form_view(request): 

    context = {}
    form = SparqlForm(request.GET or None) 
    context['form']= form 
    
    return render(request, "form.html", context)


def sparql_view(request): 

    form = SparqlForm(request.GET or None) 
    
    if form and form.is_valid():
        query_str = urllib.parse.urlencode(request.GET, doseq=True)
        
        query_url=f"{SPARQL_ENDPOINT_URL}?{query_str}"
        logger.debug("redirect to:" + query_url)
        response = requests.get(query_url)

        django_response = HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
        return django_response
    else:
        return HttpResponse({'status': 'error', 'message': 'invalid form'})
