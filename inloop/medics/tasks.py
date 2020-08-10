import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from inloop.medics.models import PlayerDetails, RankSnapshot

logger = logging.getLogger(__name__)


@db_periodic_task(crontab(hour='0', minute='0'))
def update_ranks():
    for i, player in enumerate(PlayerDetails.objects.order_by('-total_points')):
        new_rank = i + 1
        try:
            rank_snapshot = RankSnapshot.objects.get(player=player)
            delta = rank_snapshot.rank - new_rank
            rank_snapshot.rank = new_rank
            rank_snapshot.delta = delta
            rank_snapshot.save()
        except RankSnapshot.DoesNotExist:
            RankSnapshot.objects.create(player=player, rank=new_rank)
    logger.info(f'Updated ranks.')
