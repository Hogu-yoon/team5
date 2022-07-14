"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse
from ninja import NinjaAPI

from content_post.apis.v1.comment_router import content as comment_router
from content_post.apis.v1.detail_router import content as detail_router
from content_post.apis.v1.main_router import content as main_router
from content_post.apis.v1.scrap_router import content as scrap_router
from content_post.apis.v1.mypage_router import content as mypage_router
from content_post.apis.v1.weather_router import content as weather_router
from user_admission import views
from user_admission.apis.v1.login_router import account as login_router
from user_admission.apis.v1.logout_router import account as logout_router
from user_admission.apis.v1.register_router import account as register_router

from django.contrib.auth import views as auth_views

# version 1.0.0 >> 중요한 변경 / 중간 변경 / 최소 변경


api = NinjaAPI(urls_namespace="test_1", version="1.0.0", docs_url=None)

api.add_router("login/", login_router)
api.add_router("register/", register_router)
api.add_router("", main_router)
api.add_router("detail/", detail_router)
api.add_router("detail/", scrap_router)
api.add_router("logout/", logout_router)
api.add_router("comment/", comment_router)
# api.add_router("weather/", mypage_router)
api.add_router("mypage/", mypage_router)
api.add_router("k-weather/", weather_router)

urlpatterns = [
    path("tomorrow/weather/admin/", admin.site.urls),
    path("", api.urls),
    path("accounts/", include("allauth.urls")),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'),
         name="password_reset"),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name="password_reset_complete"),

    # path('', include('user_admission.urls')),
    # path('', include('content_post.urls')),
    # path("join/", views.create_user, name="create_user"),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# {% url 'xx:xxx' %} >>>>>>> reverse('api-1.0.0:login')