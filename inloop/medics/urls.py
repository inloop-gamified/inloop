from django.conf.urls import url

from inloop.medics import views

app_name = 'medics'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wiki/$', views.wiki, name='wiki'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^achievements/$', views.achievements, name='achievements'),
    url(
        r'^colleagues/add/(?P<player_details_id>[\d]+)/$',
        views.add_colleague,
        name='add_colleague'
    ),
    url(
        r'^avatars/$',
        views.avatars,
        name='avatars'
    ),
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
