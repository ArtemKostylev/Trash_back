from rest_framework import serializers
from trash.models import Post, User, Comment  

class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = ['id', 'text', 'latitude', 'longitude', 'created', 'modified', 'image', 'author']

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only' : True}}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created', 'post']

