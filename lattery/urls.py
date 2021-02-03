"""lattery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from foodball import views,views_base_sfc


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('sfcs/', views_base_sfc.get_list),
    path('fenxi/', views_base_sfc.analysis_plurl),
    path('plurls/', views_base_sfc.get_analysis_plurl_list),
    path('plurls_2/', views_base_sfc.get_analysis_plurl_list_2),
    path('plurls_3/', views_base_sfc.get_analysis_plurl_list_3),
    path('fenxi_all/', views_base_sfc.analysis_plurl_all),
    path('update_data/', views_base_sfc.update_data),
    path('get_expect_list/', views_base_sfc.get_expect_list),
    path('load_kj/', views_base_sfc.load_kj_data),
]
