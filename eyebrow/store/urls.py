

from django.urls import path
from .import views

urlpatterns = [

    path('', views.store, name = 'store'),    # type: ignore
    path('category/<slug:category_slug>/', views.store, name = 'products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>' , views.product_detail, name = 'product_detail'),
    path('search/',views.search, name='search'),
    path('review/submit-review/<int:product_id>/', views.submit_review, name='submit_review'),  # type: ignore


]
