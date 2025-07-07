from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CategoryListCreate, CategoryDetails, ItemListCreate
from django.urls import path

# router = DefaultRouter()
# router.register(r'categories', CategoryViewSet, basename='category')

# urlpatterns = router.urls
urlpatterns = [
    path('category/', CategoryListCreate.as_view(), name='category-list-create'),
    path('category/<str:pk>', CategoryDetails.as_view(), name='category-details'),
    path('item/', ItemListCreate.as_view(), name='item-list-create'),
]