from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from .models import FAQ, Post, Review
from .serializers import FAQSerializer, PostDetailSerializer, PostListSerializer, ReviewSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    lookup_field = "slug"
    pagination_class = None

    def get_serializer_class(self):
        return PostDetailSerializer if self.action == "retrieve" else PostListSerializer


class FAQListView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = None


class ReviewListView(ListAPIView):
    queryset = Review.objects.filter(is_published=True)
    serializer_class = ReviewSerializer
    pagination_class = None