
from django.urls import path
from . import views




urlpatterns = [
    path('',views.temporary,name='temporary'),
    path('ingest/', views.ingest_log, name='ingest_log'),
    path('query/', views.query_logs, name='query_logs'),
   
    
]

