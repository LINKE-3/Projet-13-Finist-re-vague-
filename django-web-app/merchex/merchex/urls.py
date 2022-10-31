"""merchex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from listings import views

from django.conf.urls import handler500, handler404

from django.conf import settings
from django.conf.urls.static import static



handler500 = 'listings.views.handler500'
handler404 = 'listings.views.handler404'

urlpatterns = [
    path("hello/", views.hello),
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('plage/<path:plage_name>', views.plage, name='plage'),
    path('register', views.registration, name='register'),
    path('connection', views.connection, name="connection"),
    path('disconnection', views.disconnection, name='logout'),
    path('mentions', views.mentions, name="mentions"),
    path('contact', views.contactsite, name='contact'),

    path('image_upload/<path:plage_name>', views.image_view, name = 'image_upload'),
    path('success', views.success, name = 'success'),

    path('contact-us/<path:plage_name>', views.contact, name='contact'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)