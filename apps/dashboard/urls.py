from django.urls import path

from .views import about, dashboard, fontes_page, home, indicadores_page

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('indicadores/', indicadores_page, name='indicadores'),
    path('fontes/', fontes_page, name='fontes'),
    path('sobre/', about, name='sobre'),
]
