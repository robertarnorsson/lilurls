from django.urls import path

from shortener import views

urlpatterns = [
    path("", views.shortener, name="shortener"),
    path('u/<str:short_url_extension>', views.redirect_url, name='redirect_url'),
    path('track/', views.tracking, name='track'),
    path('t/<str:short_url_extension>', views.track_url, name='track_url'),
    path('report/', views.report_url, name='report'),
    path('w/<str:short_url_extension>', views.rediect_warning, name='warning'),
]