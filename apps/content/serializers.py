from rest_framework import serializers

from  root.utils import pick_lang
from .models import FAQ, Post, Review


class PostListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "slug", "title", "excerpt", "cover", "published_at"]

    def get_title(self, obj):
        return pick_lang(obj, "title", self.context.get("request"))

    def get_excerpt(self, obj):
        return pick_lang(obj, "body", self.context.get("request"))[:200]


class PostDetailSerializer(PostListSerializer):
    body = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ["body"]

    def get_body(self, obj):
        return pick_lang(obj, "body", self.context.get("request"))


class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ["id", "question", "answer"]

    def get_question(self, obj):
        return pick_lang(obj, "question", self.context.get("request"))

    def get_answer(self, obj):
        return pick_lang(obj, "answer", self.context.get("request"))


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "author", "text", "rating", "created_at"]