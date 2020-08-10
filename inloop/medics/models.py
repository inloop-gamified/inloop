
from django.db import models
from django.conf import settings
from django.utils import timezone

from inloop.solutions.models import Solution, SolutionFile
from inloop.tasks.models import Task


class Medic(models.Model):
    name = models.TextField(primary_key=True)
    profession = models.TextField()

    def __str__(self):
        return f'Medic {self.name} ({self.profession})'


class Rule(models.Model):
    identifier = models.TextField(primary_key=True)

    explanation = models.TextField()

    medic = models.ForeignKey(Medic, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rule {self.identifier}'


def validate_priority(value):
    return value in ['information', 'warning', 'error']


class Violation(models.Model):
    message = models.TextField()
    priority = models.TextField(validators=[validate_priority])

    start_line = models.IntegerField(null=True, blank=True)
    end_line = models.IntegerField(null=True, blank=True)
    start_column = models.IntegerField(null=True, blank=True)
    end_column = models.IntegerField(null=True, blank=True)

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    solution_file = models.ForeignKey(SolutionFile, on_delete=models.CASCADE)

    @property
    def penalty(self):
        if self.priority == 'information':
            return 0
        if self.priority == 'warning':
            return 50
        return 100

    def __str__(self):
        return f'Violation of {self.rule} in {self.solution}'


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.TextField()
    text = models.TextField()
    style = models.TextField(default='info')

    was_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification: {self.title}'


class Level(models.Model):
    index = models.PositiveIntegerField(primary_key=True)
    points = models.PositiveIntegerField()
    name = models.TextField()

    @property
    def next(self):
        try:
            return Level.objects.get(index=self.index + 1)
        except Level.DoesNotExist:
            return None


class Avatar(models.Model):
    name = models.TextField(primary_key=True)


class PlayerDetails(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    total_points = models.PositiveIntegerField(default=0)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, null=True, blank=True)


    @property
    def percent_of_level(self):
        return 100 * (self.points_in_level / self.level.next.points)

    @property
    def points_in_level(self):
        return self.total_points - self.level.points

    @property
    def points_until_next_level(self):
        return self.level.next.points - self.total_points

    def __str__(self):
        return str(self.user)


class ColleagueTracker(models.Model):
    tracker = models.ForeignKey(
        PlayerDetails,
        related_name='tracker_set',
        on_delete=models.CASCADE
    )
    tracked_colleague = models.ForeignKey(
        PlayerDetails,
        related_name='tracked_colleague_set',
        on_delete=models.CASCADE
    )


class Badge(models.Model):
    identifier = models.TextField(primary_key=True)
    reward = models.PositiveIntegerField()
    description = models.TextField()


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.IntegerField()

    is_valid = models.BooleanField(default=True)


class SolutionScore(Score):
    solution = models.OneToOneField(Solution, null=True, blank=True, on_delete=models.CASCADE)


class BadgeScore(Score):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)


class RankSnapshot(models.Model):
    player = models.OneToOneField(
        PlayerDetails,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    rank = models.PositiveIntegerField()
    delta = models.IntegerField(default=0)
