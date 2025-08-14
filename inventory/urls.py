from .views import CategoryListCreate, CategoryDetails, ItemListCreate, ItemDetails, UserList, UserDetail, RegisterView, LoginView, StockListCreate, StockDetails, ProductListCreate, ProductDetails, OrderListCreate, OrderDetails, DashboardView, CustomRefreshToken
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
    path('auth/refresh/', CustomRefreshToken.as_view(), name='refresh'),

    path('stock/', StockListCreate.as_view(), name='stock-list-create'),
    path('stock/<str:pk>', StockDetails.as_view(), name='stock-details'),

    path('product/', ProductListCreate.as_view(), name='product-list-create'),
    path('product/<str:pk>', ProductDetails.as_view(), name='product-details'),

    path('order/', OrderListCreate.as_view(), name='order-list-create'),
    path('order/<str:pk>', OrderDetails.as_view(), name='order-details'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]