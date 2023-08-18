from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from shop.models import Category, Product, Article


class ProductDetailSerializer(ModelSerializer):
    articles = SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name", "category", "articles", "ecoscore"]

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name", "category"]



class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "date_created", "date_updated", "description"]

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError("Category already exists")
    
        return value
    
    def validate(self, data):
        if data["name"] not in data["description"]:
            raise ValidationError("Name must be in description")
        
        return data



class CategoryDetailSerializer(ModelSerializer):
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "date_created", "date_updated", "products"]

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductDetailSerializer(queryset, many=True)
        return serializer.data


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = ["id", "date_created", "date_updated", "name", "product"]

    def validate_name(self, value):
        if Article.objects.filter(name=value).exists():
            raise ValidationError("Article already exists")
    
        return value
    
    def validate(self, data):
        if data["price"] <= 1:
            raise ValidationError("Price must be above 1 €")
        elif data["product"].active == False:
            raise ValidationError("Can't add article to an inactive product")
        return data
    
    



