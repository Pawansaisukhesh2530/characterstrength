from django.urls import path
from .views import home, transcript_view, transcript_pdf

urlpatterns = [
    path('', home, name='home'),
    path('transcript/', transcript_view, name='transcript'),
    path('transcript/pdf/<str:roll_no>/', transcript_pdf, name='transcript_pdf'),
]
