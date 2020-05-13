from django.urls import include, path
from django.contrib.auth.decorators import login_required
from covidweb.apps.sparql.views import sparql_form_view, sparql_view

urlpatterns = [
    path('', sparql_form_view, name='sparql-isparql'),
    path('endpoint', sparql_view, name='sparql-endpoint')
]
