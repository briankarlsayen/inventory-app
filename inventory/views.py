from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()
    

class CategoryListCreate(APIView):
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
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
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
    def get_object(self, pk):
        try:
            return Item.objects.get(id=pk)
        except Item.DoesNotExist:
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
