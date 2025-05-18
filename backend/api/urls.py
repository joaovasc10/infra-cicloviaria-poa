from django.urls import path
from .views import BuscaPorLogradouro, BuscaPorImplantacao

urlpatterns = [
    path('busca-logradouro/', BuscaPorLogradouro.as_view(), name='busca-logradouro'),
    path('busca-implantacao/', BuscaPorImplantacao.as_view(), name='busca-implantacao'),
]