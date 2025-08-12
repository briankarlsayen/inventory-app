from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Category, Item, User, Stock, Product, Discount, Adjustment, Order
from .serializers import CategorySerializer, ItemSerializer, UserDisplaySerializer, UserSerializer, RegisterSerializer, LoginSerializer, StockSerializer, ProductSerializer, OrderSerializer, Discount, Adjustment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from bson import ObjectId
from datetime import datetime, timedelta
import calendar

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()
    

class CategoryListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = Category.objects(is_active = True)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return None
        except:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        category.is_active = False
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ItemListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item = Item.objects(is_active=True)
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ItemDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return None
        except:
            return None
        
    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        item.is_active = False
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects(is_active=True)
        serializer = UserDisplaySerializer(user, many=True)
        return Response(serializer.data)
    
class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return None
        except:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDisplaySerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            username_exist = User.objects(username=username, is_active=True).first()
            if username_exist:
                return Response({'error': 'Username already exist'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message': 'Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    authentication_classes = []  # Disable token auth
    permission_classes = [AllowAny] 
    def post(self, request):
        print('login mo to')
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects(username=username, is_active=True).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            login_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
            # login_data (refresh).data
            # user_data = UserDisplaySerializer(user).data
            return Response({'message': 'Login successful', 'access': login_data['access'], 'refresh': login_data['refresh']}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)        
    
class StockListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item = Stock.objects(is_active=True).order_by('-updated_at')
        serializer = StockSerializer(item, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StockDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Stock.objects.get(id=pk)
        except Stock.DoesNotExist:
            return None
        except:
            return None
        
    def get(self, request, pk):
        stock = self.get_object(pk=pk)
        if not stock:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock)
        return Response(serializer.data)
    
    def put(self, request, pk):
        stock = self.get_object(pk)
        if not stock:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        stock = self.get_object(pk=pk)
        if not stock:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        stock.is_active = False
        stock.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item = Product.objects(is_active=True).order_by('-updated_at')
        serializer = ProductSerializer(item, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetails(APIView):

    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return None
        except:
            return None
        
    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        item.is_active = False
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrderListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item = Order.objects(is_active=True).order_by('-updated_at')
        serializer = OrderSerializer(item, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        request.data['processed_by'] = str(request.user.id)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderDetails(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return None
        except:
            return None
        
    def get(self, _request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        request.data['processed_by'] = str(request.user.id)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        item.is_active = False
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DashboardView(APIView):
    def get(self, request):
        total_sales = sum(order.total_amount for order in Order.objects(is_active=True))

        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())  # Monday
        start_of_year = datetime(now.year, 1, 1)

        week_count = Order.objects(date__gte=start_of_week, is_active = True).count()
        year_count = Order.objects(date__gte=start_of_year, is_active = True).count()

        weekly_sales = {}
        for order in Order.objects(date__gte=start_of_week, is_active = True):
            for p in order.products:
                prod_id = str(p.product.id)
                weekly_sales[prod_id] = weekly_sales.get(prod_id, 0) + p.quantity

        yearly_sales = {}
        for order in Order.objects(date__gte=start_of_year, is_active = True):
            for p in order.products:
                prod_id = str(p.product.id)
                yearly_sales[prod_id] = yearly_sales.get(prod_id, 0) + p.quantity

        product_ids = set(list(weekly_sales.keys()) + list(yearly_sales.keys()))

        products_map = {
            str(prod.id): {
                "name": prod.name,
                "size": prod.size,
                "type": prod.type
            }
            for prod in Product.objects(id__in=product_ids)
        }


        weekly_top_products = [
            {
                "product": pid,
                "name": products_map.get(pid, {}).get("name", "Unknown"),
                "size": products_map.get(pid, {}).get("size", None),
                "type": products_map.get(pid, {}).get("type", None),
                "quantity": qty

            }
            for pid, qty in sorted(weekly_sales.items(), key=lambda x: x[1], reverse=True)
        ]

        yearly_top_products = [
            {
                "product": pid,
                "name": products_map.get(pid, {}).get("name", "Unknown"),
                "size": products_map.get(pid, {}).get("size", None),
                "type": products_map.get(pid, {}).get("type", None),
                "quantity": qty
            }
            for pid, qty in sorted(yearly_sales.items(), key=lambda x: x[1], reverse=True)
        ]

        return Response({ 
            "total_sales": total_sales,
            "orderCount": {
                "week": week_count,
                "year": year_count
            },
            "topProducts": {
                "week": weekly_top_products,
                "year": yearly_top_products
            }}, status=status.HTTP_200_OK)        
