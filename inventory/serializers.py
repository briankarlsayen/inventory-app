from rest_framework import serializers
from .models import Category, Item, User

class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(default=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Category(**validated_data).save()
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    
class CategoryDisplaySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    
class ItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    category = serializers.CharField(required=True, write_only=True)
    category_details = CategoryDisplaySerializer(read_only=True)
    unit = serializers.CharField(required=False, allow_blank=True)
    reorder_level=serializers.IntegerField(required=False, default=0)
    is_shown = serializers.BooleanField(required=False, default=True)
    is_active = serializers.BooleanField(required=False, default=True)


    def to_representation(self, instance):
        """Customize the output to include nested category details."""
        ret = super().to_representation(instance)
        ret['category_details'] = CategoryDisplaySerializer(instance.category).data
        return ret

    def create(self, validated_data):
        category_id = validated_data.get('category')
        category = Category.objects.get(id=category_id)
        validated_data['category'] = category

        item = Item(**validated_data)
        return item.save()
    def update(self, instance, validated_data):
        if 'category' in validated_data:
            instance.category = Category.objects.get(id=validated_data.get('category'))
        instance.name = validated_data.get('name', instance.name)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.reorder_level = validated_data.get('reorder_level', instance.reorder_level)
        instance.is_shown = validated_data.get('is_shown', instance.is_shown)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    

class UserDisplaySerializer(serializers.Serializer):
    id= serializers.CharField(read_only=True)
    name= serializers.CharField(read_only=True)
    username= serializers.CharField(read_only=True)
    role= serializers.IntegerField(read_only=True)

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    username = serializers.CharField(read_only=True)
    role = serializers.IntegerField(default=2, read_only=True)
    is_active = serializers.BooleanField(required=False, default=True)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.username = validated_data.get('username', instance.username)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.ChoiceField(default=2, choices=[1,2])

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(raw_password)
        return user.save()
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.IntegerField(read_only=True, required=False)
    
    