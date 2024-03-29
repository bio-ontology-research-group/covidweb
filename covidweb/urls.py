"""covidweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from covidweb.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('upload/', include('uploader.urls')),
    path('isparql/', include('sparql.urls')),
    path('manage/', include('covidweb.manage_urls')),
    path('api/', include('covidweb.api_urls')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('doc/', TemplateView.as_view(template_name='doc.html'), name='documentation'),
    path('healthcheck', TemplateView.as_view(template_name='health.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
