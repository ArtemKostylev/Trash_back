from django.contrib import admin
from django.urls import path
from trash import views
import trash_dev.settings as settings
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    #TODO dev only, remove in production
    path('api/get-users/', views.get_users, name='get_users'),
    path('api/post/', views.post_api_view, name='post_api'),
    path('api/create-user/', views.create_user, name = 'create_user'),
    path('api/user/', views.user_authenticated_api, name = 'modify_user'),
    path('api/comment/', views.comment_api_view, name = 'comment_api'),
    path('api/post-comments/', views.post_comments, name = "post_commentaries"),
    path('api/user-comments/', views.user_comments, name = "user_commentaries"),
    path('api/user-posts/', views.user_posts, name = "user_posts"),
    path('api/obtain-auth-token/', obtain_jwt_token, name = 'obtain_auth_token'),
    path('api/refresh-auth-token/', refresh_jwt_token, name = 'refresh_auth_token')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()