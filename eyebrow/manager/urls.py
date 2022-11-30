from django.urls import path
from .import views

urlpatterns = [
    path('dashbord/',views.manager_dashboard, name="manager_dashboard"),
    path('admin_change_password/',views.admin_change_password,name="admin_change_password"),

    #USER MANAGEMENT
    path('user_management/',views.user_management,name="user_management"),
    path('block_user/<int:user_id>/',views.block_user,name="block_user"),
    path('unblock_user/<int:user_id>/',views.unblock_user,name="unblock_user"),

    #PRODUCT MANAGEMENT
    path('product_management/',views.product_management,name='product_management'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),

    #ORDER MANAGEMENT
    path('order_management/', views.order_management, name="order_management"),
    path('manager_vieworder/<str:tracking_no>/', views.manager_vieworder, name='manager_vieworder'),
    path('manager_accept_order/<str:tracking_no>/', views.manager_accept_order, name='manager_accept_order'),
    path('manager_ship_order/<str:tracking_no>/', views.manager_ship_order, name='manager_ship_order'),
    path('manager_delivered_order/<str:tracking_no>/', views.manager_delivered_order, name='manager_delivered_order'),
    path('manager_cancel_order/<str:tracking_no>/', views.manager_cancel_order, name='manager_cancel_order'),

    #CATEGORY MANAGEMENT
    path('category_management/', views.category_management, name="category_management"),
    path('add_category/', views.add_category, name='add_category'),
    path('update_category/<int:category_id>/', views.update_category, name="update_category"),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),

    # VARIATION MANAGEMENT
    path('variation_management/', views.variation_management, name="variation_management"),
    path('add_variation/', views.add_variation, name='add_variation'),
    path('update_variation/<int:variation_id>/',views.update_variation,name='update_variation'),
    path('delete_variation/<int:variation_id>/', views.delete_variation, name='delete_variation'),

    #REVIEW MANAGER
    path('review_management/',views.review_management,name='review_management'),
    path('review_block/<int:review_id>/',views.review_block,name='review_block'),
    path('review_unblock/<int:review_id>/',views.review_unblock,name='review_unblock'),

    #HOME PAGE
    #BANNER
    path('banner_management/',views.banner_management,name='banner_management'),
    path('add_banner/',views.add_banner,name='add_banner'),
    path('update_banner/<int:banner_id>/',views.update_banner,name='update_banner'),
    path('delete_banner/<int:banner_id>/',views.delete_banner,name='delete_banner'),

    #BRANDADS
    path('brandads_management/',views.brandads_management,name='brandads_management'),
    path('add_brandads/',views.add_brandads,name='add_brandads'),
    path('update_brandads/<int:brandads_id>/',views.update_brandads,name='update_brandads'),
    path('delete_brandads/<int:brandads_id>/',views.delete_brandads,name='delete_brandads'),
    


    
]
