from django.urls import path

from clients.views import (
    ClientCreateView, 
    DeleteClientView, 
    ListClientsView
)

urlpatterns = [
    path('all/', ListClientsView.as_view(), name="list_clients"),
    path('new/', ClientCreateView.as_view(), name="new_client"),
    path('delete/<int:pk>/', DeleteClientView.as_view(), name="delete_client")
]