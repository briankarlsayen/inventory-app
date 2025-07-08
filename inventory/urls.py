from .views import CategoryListCreate, CategoryDetails, ItemListCreate, ItemDetails, UserList, UserDetail, RegisterView, LoginView
from django.urls import path


urlpatterns = [
    path('category/', CategoryListCreate.as_view(), name='category-list-create'),
    path('category/<str:pk>', CategoryDetails.as_view(), name='category-details'),
    
    path('item/', ItemListCreate.as_view(), name='item-list-create'),
    path('item/<str:pk>', ItemDetails.as_view(), name='item-details'),

    path('user/', UserList.as_view(), name='user-list'),
    path('user/<str:pk>', UserDetail.as_view(), name='user-details'),

    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
]