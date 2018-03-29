from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^$', views.me, name="me"),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    # url(r'^tf/submit/(?P<source>[register|login]+)', views.two_factor_view, name='two-factor-verification'),
    url(r'tf/submit/$', views.two_factor_view, name='tfv'),
]
