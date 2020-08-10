from django.conf.urls import url

from inloop.medics import views

app_name = 'medics'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wiki/$', views.wiki, name='wiki'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(
        r'^consultation/(?P<solution_id>[\d]+)/$',
        views.consultation,
        name='consultation'
    ),
    url(
        r'^progress/(?P<user_id>[\d]+)/$',
        views.progress,
        name='progress'
    ),
]
