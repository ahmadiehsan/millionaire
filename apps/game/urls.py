from django.urls import path, re_path

from helpers.constants import UUID_REGEX
from .views import GameSpaceView, ResultView

app_name = 'game'

urlpatterns = [
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
