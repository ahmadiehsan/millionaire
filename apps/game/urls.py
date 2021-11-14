from django.urls import path, re_path

from helpers.constants import UUID_REGEX
from .views import GameSpaceView, ResultView, StatisticsView

app_name = 'game'

urlpatterns = [
    path('', StatisticsView.as_view(), name='statistics'),
    path(
        'result/<game_id>',
        ResultView.as_view(),
        name='result'
    ),
    re_path(
        r'(?P<game_identifier>({uuid_regex}|new))'.format(uuid_regex=UUID_REGEX),
        GameSpaceView.as_view(),
        name='game-space'
    ),
]
