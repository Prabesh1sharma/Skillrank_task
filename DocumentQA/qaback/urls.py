from django.urls import path
from .views import upload_pdf, ask_question, chat_view

urlpatterns = [
    path("", chat_view, name="chat"),
    path("upload_pdf/", upload_pdf, name="upload_pdf"),
    path("ask_question/", ask_question, name="ask_question"),
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)