from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from uploader.forms import UploadForm
from covidweb.mixins import FormRequestMixin
from uploader.models import Upload
from uploader.utils import api


class UploadCreateView(FormRequestMixin, CreateView):

    model = Upload
    form_class = UploadForm
    template_name = 'uploader/form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UploadCreateView, self).get_context_data(*args, **kwargs)
        return context

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self, *args, **kwargs):
        return reverse('uploader-view', kwargs={'pk': self.object.pk})


class UploadDetailView(DetailView):
    model = Upload
    template_name = 'uploader/view.html'


class UploadListView(ListView):
    model = Upload
    template_name = 'uploader/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(col_uuid__isnull=False)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
    
