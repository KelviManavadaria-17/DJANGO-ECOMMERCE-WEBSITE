from django import forms
from django.urls import path
from django.utils.translation import templatize
from store import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .form import LoginForm, MyPasswordChangeForm, MyPasswordResetForm , MySetPasswordForm
urlpatterns = [
    # path('', views.home,name="home"),
    path('',views.ProductView.as_view(),name="home"),
    path('removeitem/',views.RemoveItem,name='removeitem'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name="show_cart"),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    path('add_one/<int:pk>',views.add_one,name='add_one'),
    path('remove_one/<int:pk>',views.remove_one,name='remove_one'),
    path('paymentdone',views.paymentdone,name="paymentdone"),


    path('accounts/login/',auth_views.LoginView.as_view(template_name = 'store/login.html',authentication_form = LoginForm ),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(next_page = 'login'),name='logout'),
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='store/changepassword.html',form_class=MyPasswordChangeForm , success_url = '/changepasswordDone/'),name='changepassword'),
    path('changepasswordDone/',auth_views.PasswordChangeView.as_view(template_name='store/changepasswordDone.html'),name='changepasswordDone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='store/password_reset.html' ,form_class = MyPasswordResetForm , ),name='password-reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'),name='password_reset_done'),
    path('password_reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html',form_class = MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'),name='password_reset_complete'),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)