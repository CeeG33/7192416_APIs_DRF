from rest_framework.serializers import ModelSerializer, SerializerMethodField

from shop.models import Category, Product, Article


class ProductDetailSerializer(ModelSerializer):
    articles = SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name", "category", "articles"]

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name"]



class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "date_created", "date_updated"]



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
        fields = ["id", "date_created", "date_updated", "name", "price", "product"]


