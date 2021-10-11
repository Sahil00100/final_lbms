from django.urls import path
from.views import index_view,signup_view,login_view,logout_view,product_view,order_view,order_delete,rate_and_review,list_books,filter_search,latest,otp_view,resend_otp
from django.conf.urls.static import static
from.views import membership,paymenthandler,membership_result,profile_view,combetition,publish_view,orders,penalty_view,penalty_handler,cart_view,cart,cart_delete
from django.conf import settings
import os

urlpatterns = [
  
  path('index/',index_view,name="index"),
  path('signup/',signup_view,name="signup"),
  path('otp/<str:name_of_user>/',otp_view,name="otp"),
  path('otp2/<str:name_of_user>/',resend_otp,name="otp2"),
  path('login/',login_view,name='login'),
  path('membership/',membership,name='membership'),
  path('logout/',logout_view,name='logout'),
  path('product/<str:name_of_book>/',product_view,name='product'),
  path('order/<str:name_of_book>/',order_view,name='order'),
  path('delete/<str:name_of_book>/',order_delete,name='delete'),
  path('rate/<str:name_of_book>/',rate_and_review,name='rate'),
  path('listproducts/',list_books,name='list'),
  path('filter/<str:category>/',filter_search,name='filter'),
  path('latest/',latest,name='latest'),
  path('paymenthandler/', paymenthandler, name='paymenthandler'),
  path('result/', membership_result, name='result'),
  path('profile/', profile_view, name='profile'),
  path('comb/<str:name_of_combetition>', combetition, name='comb'),
  path('publish/', publish_view, name='publish'),
  path('orders/', orders, name='orders'),
  path('penalty/', penalty_view, name='penalty'),
  path('penaltyhandler/', penalty_handler, name='penaltyhandler'),
  path('cart/', cart_view, name='cart'),
  path('cartsaving/<str:name_of_book>', cart, name='cart2'),
  path('cartdelete/<str:name_of_book>', cart_delete, name='cartdelete'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
