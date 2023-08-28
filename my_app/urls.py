from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-signup', views.user_signup, name='signup'),
    path('add-new-post', views.add_new_post, name='add_new_post'),
    path('user-profile', views.user_profile, name='user_profile'),
    path('update-post/<int:post_id>', views.update_post, name='update_post'),
    path('deactivate-post/<int:post_id>', views.deactivate_post, name='deactivate_post'),
    path('activate-post/<int:post_id>', views.activate_post, name='activate_post'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('update-profile', views.update_profile, name='update_profile'),
    path('post-detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('login-user', views.login_user, name='login'),
    path('logout-user', views.user_logout, name='logout'),
    path('about-us', views.about_us, name='about_us'),
    path('contact-us', views.contact_us, name='contact_us'),
    path('donation/<int:post_id>', views.donation, name='donation'),
    path('received-donations', views.received_donations, name='received_donations'),
    path('approve-donation/<int:donation_id>', views.approve_donation, name='approve_donation'),
    path('notifications', views.notifications, name='notifications')
]
