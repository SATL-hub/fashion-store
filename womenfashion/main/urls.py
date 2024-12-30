
from django.urls import path
from . import views
urlpatterns = [
   
    path('',views.home,name="home"),
    path('api/products/<str:category_name>/', views.filter_products, name='filter_products'),
    path('product-filter/<str:name>/<str:a>/',views.product_details, name="product_details"),
    path('filter_products_by_price/', views.filter_products_by_price, name='filter_products_by_price'),
    path('userlogin/',views.userlogin,name="userlogin"),
    path('register/',views.register,name='userregister'),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('profile/<int:id>/',views.profile,name="profile"),
    path('cart/',views.cart,name="cart"),
    path('contact/',views.contact,name='contact'),
    path('product_detail/<int:id>/',views.details,name='product_detail'),
    path('minuscart/<de>',views.minuscart,name="minuscart"),
    path('pluscart/<de>',views.pluscart,name="pluscart"),
    path('delecart/<de>',views.deletecart,name="deletecart"),
    path('check_out/<int:id>/',views.check_out,name='check_out'),
    path('wishlist/<int:id>/',views.wishlist,name='wishlist'),
    path('wishlists/<int:id>',views.wishlists,name='wishlists'),
    path('shop',views.shop,name='shop'),
    path('product_revirew/<int:id>/',views.product_review,name='product_review'),
    path('changepassword/',views.changepassword,name = 'changepassword'),
    path('history/',views.history,name='history')

]
