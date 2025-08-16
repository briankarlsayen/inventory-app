from rest_framework import serializers
from .models import  Item, User, Stock, OrderedProduct, Order, Discount, Adjustment, Product
from datetime import datetime, timezone

class ItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    category = serializers.CharField()
    unit = serializers.CharField(required=False, allow_blank=True)
    reorder_level=serializers.IntegerField(required=False, default=0)
    is_shown = serializers.BooleanField(required=False, default=True)
    is_active = serializers.BooleanField(required=False, default=True)

    def validate_name(self, value):
        # For create (self.instance is None)
        if not self.instance and Item.objects(name__iexact=value).first():
            raise serializers.ValidationError("Item name already exists.")
        # For update (self.instance exists, so exclude it from the check)
        if self.instance and Item.objects(name__iexact=value, id__ne=self.instance.id).first():
            raise serializers.ValidationError("Item name already exists.")
        return value

    def create(self, validated_data):
        item = Item(**validated_data)
        return item.save()
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
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
    
class ItemDisplaySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    unit = serializers.CharField(read_only=True)
    reorder_level = serializers.IntegerField(read_only=True)

class StockSerializer(serializers.Serializer):
    id= serializers.CharField(read_only=True)
    type = serializers.ChoiceField(default="entry", choices=['entry', 'usage'])
    item = serializers.CharField(required=True, write_only=True)
    item_details = ItemDisplaySerializer(read_only=True)
    quantity = serializers.IntegerField(required=True)
    remarks = serializers.CharField(required=False)
    date = serializers.DateTimeField()
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        """Customize the output to include nested category details."""
        ret = super().to_representation(instance)
        ret['item_details'] = ItemDisplaySerializer(instance.item).data
        return ret

    def validate_item(self, value):
        try:
            Item.objects.get(id=value)
            return value
        except:
            raise serializers.ValidationError("Invalid item ID.")

    def create(self, validated_data):
        item_id = validated_data.get('item')
        item = Item.objects.get(id=item_id)
        validated_data['item'] = item
        return Stock(**validated_data).save()
    
    def update(self, instance, validated_data):
        if 'item' in validated_data:
            instance.item = Item.objects.get(id=validated_data.get('item'))
    
        instance.type = validated_data.get('type', instance.type)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.date = validated_data.get('date', instance.date)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.updated_at = datetime.now(timezone.utc)
        instance.save()
        return instance
    
class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    size = serializers.ChoiceField(choices=["8oz", "12oz", "16oz", ""])
    price = serializers.FloatField(required=True)
    type = serializers.ChoiceField(required=True, choices=["drink", "pastry", "others"])
    is_active = serializers.BooleanField(required=False, default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        product = Product(**validated_data)
        return product.save()
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.size = validated_data.get('size', instance.size)
        instance.price = validated_data.get('price', instance.price)
        instance.type = validated_data.get('type', instance.type)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class DiscountSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    value = serializers.FloatField(required=True)
    type = serializers.ChoiceField(required=True, choices=["fixed", "percentage"])

class AdjustmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    value = serializers.FloatField(required=True)

class ProductDisplaySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    size = serializers.CharField(read_only=True)
    price = serializers.FloatField(read_only=True)

class OrderedProductSerializer(serializers.Serializer):
    product = serializers.CharField(required=True, write_only=True)
    product_details = ProductDisplaySerializer(read_only=True)
    quantity = serializers.IntegerField(required=True)
    purchase_price = serializers.FloatField(required=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['product_details'] = ProductDisplaySerializer(instance.product).data
        return ret

class DiscountDisplaySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    value = serializers.FloatField(read_only=True)
    note = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)

class AdjustmentDisplaySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    value = serializers.FloatField(read_only=True)
    note = serializers.CharField(read_only=True)

class OrderSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    products = OrderedProductSerializer(many=True)
    total_amount = serializers.FloatField(required=True)
    payment_type = serializers.ChoiceField(required=True, choices=["cash", "gcash", "card"])
    processed_by = serializers.CharField(source="processed_by.id", write_only=True)
    discount_details = serializers.DictField(required=False, child=serializers.CharField(), write_only=True)
    discount = serializers.CharField(required=False, write_only=True)
    adjustment_details = serializers.DictField(required=False, child=serializers.CharField(), write_only=True)
    adjustment = serializers.CharField(required=False, write_only=True)
    is_active = serializers.BooleanField(required=False, default=True)
    date = serializers.DateTimeField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['processed_by'] = UserDisplaySerializer(instance.processed_by).data['name']
        ret['discount_details'] = DiscountDisplaySerializer(instance.discount).data or None
        ret['adjustment_details'] = AdjustmentDisplaySerializer(instance.adjustment).data or None
        return ret


    def create(self, validated_data):
        products_data = validated_data.get('products')
        discount_details = validated_data.pop('discount_details', None)
        adjustment_details = validated_data.pop('adjustment_details', None)
        processed_by = validated_data.pop('processed_by', None)

        validated_data['processed_by'] = User.objects.get(id=processed_by['id'])

        if discount_details:
            discount = Discount(
                type=discount_details.get('type', 'fixed'),
                value=float(discount_details.get('value', 0)),
                note=discount_details.get('note', ''),
            )
            discount.save()
            validated_data['discount'] = discount

        if adjustment_details:
            adjustment = Adjustment(
                value=float(adjustment_details.get('value', 0)),
                note=adjustment_details.get('note', ''),
            )
            adjustment.save()
            validated_data['adjustment'] = adjustment


        order = Order(**validated_data)

        order.products = [
            OrderedProduct(**product) for product in products_data
        ]
        order.save()
        return order
    
    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', None)
        discount_details = validated_data.pop('discount_details', None)
        adjustment_details = validated_data.pop('adjustment_details', None)
        processed_by = validated_data.pop('processed_by', None)
        validated_data['updated_at'] = datetime.now(timezone.utc)

        if discount_details is None: # if it is undefined, do nothing
            pass 
        elif discount_details == {}: # if empty {}, delete ref id
            validated_data['discount'] = None
        elif isinstance(discount_details, dict): # if with value, create new discount
            discount = Discount(
                type=discount_details.get('type', 'fixed'),
                value=float(discount_details.get('value', 0)),
                note=discount_details.get('note', ''),
            )
            discount.save()
            validated_data['discount'] = discount

        if adjustment_details is None: # if it is undefined, do nothing
            pass 
        elif adjustment_details == {}: # if empty {}, delete ref id
            validated_data['adjustment'] = None
        elif isinstance(adjustment_details, dict): # if with value, create new adjustment
            adjustment = Adjustment(
                value=float(adjustment_details.get('value', 0)),
                note=adjustment_details.get('note', ''),
            )
            adjustment.save()
            validated_data['adjustment'] = adjustment

        instance['processed_by'] = User.objects.get(id=processed_by['id'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if products_data is not None:
            instance.products = [
                OrderedProduct(**product) for product in products_data
            ]

        instance.save()
        return instance