"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'main'

urlpatterns = [
    path("",views.homepage,name='homepage'),
    path("register/",views.register,name='register'),
    path("logout/",views.logout_request,name='logout'),
    path("login/",views.login_request,name='login'),
    path("capture/",views.capture,name="capture"),
    path("detect/",views.detect,name="detect"),
    path('image/',views.image,name='click'),
    path('image/process/',views.process,name='process'),
    path('results/',views.results,name='results'),
    path('details/',views.details,name='details'),
    # path('capture2/image/',views.image,name='image'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()