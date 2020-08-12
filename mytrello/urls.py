from django.urls import path

from mytrello import views

urlpatterns = [
    path('', views.Index.as_view(), name='homepage'),
    path('new/', views.NewCardView.as_view(), name='new_card'),
    path('edit/<int:pk>', views.EditCard.as_view(), name='edit_card'),
    path('delete/<int:pk>', views.DeleteCard.as_view(), name='delete_card'),
]
