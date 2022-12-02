import os.path

from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django_extensions.settings import BASE_DIR

from . import views

app_name = "chat"
urlpatterns = [
    path("", views.HomeView.as_view(), name="main"),
    path('jsonfun', views.jsonfun, name='jsonfun'),
    path('syntax', TemplateView.as_view(template_name="chat/templates/chat/syntax.html"), name='syntax'),
    path('talk', views.TalkMain.as_view(), name='talk'),
    path('messages', views.TalkMessages.as_view(), name='messages'),
    path("log", views.log, name='log'),
    path("login", views.log_in, name="log_in"),

    # Serve up a local static folder to serve spinner.gif
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(BASE_DIR, 'static'), 'show_indexes': True},
            name='static')

]
