from rest_framework import serializers
from .models import Posts

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.username')
    class Meta: 
        model = Posts
        fields = ['id', 'author', 'title', 'content', 'image']