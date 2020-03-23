from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import user_logged_in
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes

from rest_framework_jwt.settings import api_settings

from trash_dev import settings
from trash.models import Post, User, Comment
from trash.serializers import PostSerializer, UserSerializer, CommentSerializer

import datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class GetUserData(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'user': 'test'}

       
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, ]) 
def post_api_view(request):
    pk = request.GET.get('pk', '')
    if request.method == 'GET':
        timestamp = request.GET.get('timestamp', '')
               
        if pk: 
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)   
            serializer = PostSerializer(post)
            return JsonResponse(serializer.data, safe = False)
        elif timestamp:
            timestamp = timestamp.replace('Z', '')
            timestamp = datetime.datetime.fromisoformat(timestamp)
            posts = Post.objects.filter(Q(created__gte = timestamp) | Q(modified__gte = timestamp))
        else: 
            posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        return JsonResponse(serializer.data, safe = False)

    elif request.method == 'POST':
        data = request.data
        serializer = PostSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(status.HTTP_201_CREATED)

    elif request.method == 'PUT':        
        data = request.data
        try: 
            post = Post.objects.get(pk = data['id'])
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()   
        return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
       
    elif request.method == 'DELETE':
        if pk:
            try: 
                post = Post.objects.get(pk = pk)
            except Post.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND) 
            post.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)  
             
    else: 
        return Response(status = status.HTTP_400_BAD_REQUEST)   

@api_view(['POST'])
@permission_classes([AllowAny, ])
def create_user(request):
    user = request.data
    serializer = UserSerializer(data = user)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    
    phone_number = request.data['phone_number']

    user = User.objects.get(phone_number = phone_number)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    res = {}
    res['first_name'] = request.data['first_name']
    res['last_name'] = request.data['last_name']
    res['token'] = token

    return Response(res, status = status.HTTP_201_CREATED)

#TODO Debug only method. Delete on deployment
@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return JsonResponse(serializer.data, safe = False)

@api_view(['PUT', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated,])
def user_authenticated_api(request):
    pk = request.GET.get('pk', '')
    if pk: 
        try: 
            user = User.objects.get(id = pk)
        except User.DoesNotExist:
            return Response(status = status.HTTP_204_NO_CONTENT)
        
        if request.method == 'GET':  
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)            
        
        elif request.method == 'DELETE':
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
                    
    elif request.method == 'PUT':
        data = request.data
        pk = data['id']
        try: 
            user = User.objects.get(id = pk)
        except User.DoesNotExist:
            return Response(status = status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user, data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)

    else: 
        return Response(status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_api_view(request):
    pk = request.GET.get('id', '')
    if pk:
        try: 
            comment = Comment.objects.get(pk = pk) 
        except Comment.DoesNotExist:
            return Response(status = status.HTTP_204_NO_CONTENT)
        
        if request.method == 'GET':
            serializer = CommentSerializer(comment)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
            comment.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'POST':
        data = request.data
        serializer = CommentSerializer(data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)

    elif request.method == 'PUT':    
        data = request.data
        pk = data['id']
        try: 
            comment = Comment.objects.get(pk = pk) 
        except Comment.DoesNotExist:
            return Response(status = status.HTTP_204_NO_CONTENT)
        serializer = CommentSerializer(comment, data)
        serializer.is_valid(raise_exception = True)
        serializer.save()    
        return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)

    else: 
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_comments(request):
    post_id = request.GET['post_id']
    if post_id:
        comments = Comment.objects.filter(post_id = post_id)
        serializer = CommentSerializer(comments, many = True)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK)
    else: 
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_comments(request):
    user_id = request.GET['user_id']
    if user_id:
        comments = Comment.objects.filter(author_id = user_id)
        serializer = CommentSerializer(comments, many = True)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK)
    else: 
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request):
    user_id = request.GET['user_id']
    if user_id:
        posts = Post.objects.filter(author_id = user_id)
        serializer = CommentSerializer(posts, many = True)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK)
    else: 
        return Response(status = status.HTTP_400_BAD_REQUEST)
