from django.contrib import admin
from django.urls import path, include

from main_app import views as app_views
from accounts import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('api', include('main_app.api.urls')),

    path('profile/<int:pk>', app_views.AuthorDetailView.as_view(), name='profile'),
    path('creation/', app_views.CreationListView.as_view(), name='creation_list'),
    path('creation/new', app_views.CreationCreateView.as_view(), name='creation_new'),
    path('creation/<int:pk>', app_views.CreationDetailView.as_view(), name='creation_detail'),
    path('creation/<int:pk>/download', app_views.creation_download, name="download_page"),
    path('download/report', app_views.DownloadReportView.as_view(), name="download_report"),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
