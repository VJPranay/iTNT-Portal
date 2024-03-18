"""ldevcatalyst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from datarepo.views import districts,institutions
from common.views import not_found

admin.site.site_header = 'iTNT Super Admin'  # This will appear on the top of the admin page
admin.site.site_title = 'iTNT Super Admin'  # This is used for the title of the admin window (e.g., in the browser tab)
admin.site.index_title = 'iTNT Super Admin' 


urlpatterns = [
    path('admin/test34345/', admin.site.urls,name="django_admin"),
    path('districts/', districts,name="districts"),
    path('institutions/', institutions,name="institutions"),
    path('dashboard/', include('dashboard.urls')),
    path('innovation-challenge/', include('innovation_challenges.urls')),
    path('registrations/', include('registrations.urls')),
    path('profiles/', include('profiles.urls')),
    path('meetings/', include('meetings.urls')),
    path('common/', include('common.urls')),
    path('support/', include('support.urls')),
    path('reports/', include('reports.urls')),
    path('', not_found),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
