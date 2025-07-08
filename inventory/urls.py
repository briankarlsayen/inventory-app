from .views import CategoryListCreate, CategoryDetails, ItemListCreate, ItemDetails
from django.urls import path


urlpatterns = [
    path('category/', CategoryListCreate.as_view(), name='category-list-create'),
    path('category/<str:pk>', CategoryDetails.as_view(), name='category-details'),
    path('item/', ItemListCreate.as_view(), name='item-list-create'),
    path('item/<str:pk>', ItemDetails.as_view(), name='item-details'),
]