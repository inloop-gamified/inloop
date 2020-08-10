from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction, models

from huey.contrib.djhuey import db_task

from inloop.medics.models import Badge, BadgeScore, Violation, Notification, SolutionScore, PlayerDetails, Level, Score
from inloop.solutions.models import Solution


@db_task()
def update_player_points_and_level_async(user):
    update_player_points_and_level(user)


def update_player_points_and_level(user):
    total_points = Score.objects\
        .filter(user_id=user.id, is_valid=True)\
        .aggregate(models.Sum('points'))\
        .get('points__sum')
    level = Level.objects\
        .filter(points__lte=total_points)\
        .order_by('points')\
        .last()
    try:
        player_details = PlayerDetails.objects.get(user=user)
        player_details.total_points = total_points
        player_details.level = level
        player_details.save()
    except PlayerDetails.DoesNotExist:
        player_details = PlayerDetails.objects.create(
            user=user, total_points=total_points, level=level
        )


def dispatch_solution_score_notification(score: SolutionScore):
    task = score.solution.task
    if score.points == task.achievable_points:
        title = f'You scored {score.points} points!'
        text = f'Your solution on {task.title} scored a perfect {score.points} points!'
        style = 'success'
    elif score.points > 0:
        title = f'You scored {score.points} points!'
        text = f'Your solution on {task.title} scored {score.points} points! ' + \
               'Visit the medics to improve this score!'
        style = 'info'
    elif score.points == 0:
        title = f"Your solution on {task.title} succeeded, but didn't score any points."
        text = 'Visit the medics to fix the health issues!'
        style = 'warning'
    else:
        title = f"Your solution on {task.title} succeeded, but it's health cost " + \
                f"you {abs(score.points)} points."
        text = f'Visit the medics to fix the health issues!'
        style = 'danger'

    Notification.objects.create(user=score.user, title=title, text=text, style=style)


def dispatch_badge_score_notification(score: BadgeScore):
    badge = score.badge
    title = f'You achieved the badge "{badge.identifier}" and gained {badge.reward} points!'
    text = f'{badge.description}'
    style = 'success'
    Notification.objects.create(user=score.user, title=title, text=text, style=style)


def reward_points_for_solution_submitted(solution: Solution):
    if not solution.passed:
        return

    violation_penalty = sum(v.penalty for v in Violation.objects.filter(solution=solution))
    points = max(0, solution.task.achievable_points - violation_penalty)

    with transaction.atomic():
        # invalidate all previous scores on this task
        SolutionScore.objects\
            .filter(solution__task_id=solution.task_id)\
            .update(is_valid=False)

        score = SolutionScore.objects.create(
            solution=solution, user=solution.author, points=points
        )

    dispatch_solution_score_notification(score)

    update_player_points_and_level_async(solution.author)


def reward_badge(user, badge_identifier):
    badge = Badge.objects.get(identifier=badge_identifier)
    badge_score, created = BadgeScore.objects.get_or_create(
        user=user, badge=badge, points=badge.reward
    )
    if created:
        dispatch_badge_score_notification(badge_score)

        update_player_points_and_level_async(user)
