from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

from inloop.solutions.models import Solution
from inloop.tasks.models import Task
from inloop.medics.models import Avatar, Violation, Medic, Score, PlayerDetails, Level, ColleagueTracker

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator


@login_required
def wiki(request):
    return TemplateResponse(request, 'medics/wiki.html', {
        'medics': Medic.objects.all()
    })


@login_required
def index(request):
    solutions = []
    for task in Task.objects.all():
        solution = Solution.objects\
            .select_related('task')\
            .filter(task=task, author=request.user)\
            .order_by('-id')\
            .first()
        if not solution:
            continue
        solutions.append(solution)
    return TemplateResponse(request, 'medics/index.html', {
        'solutions': solutions
    })


@login_required
def consultation(request, solution_id):
    solution = get_object_or_404(Solution, pk=solution_id)
    if not request.user == solution.author:
        raise Http404
    violations = Violation.objects.filter(solution=solution)
    paginator = Paginator(violations, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return TemplateResponse(request, 'medics/consultation.html', {
        'page_obj': page_obj,
        'solution': solution
    })


@login_required
def progress(request, user_id):
    player_details = get_object_or_404(PlayerDetails, user_id=user_id)
    return TemplateResponse(request, 'medics/progress.html', {
        'player_details': player_details
    })


@login_required
def leaderboard(request):
    players = PlayerDetails.objects\
        .order_by('-total_points')\
        .select_related('user')
    query = request.GET.get('query')
    if query:
        players = players.filter(user__username__icontains=query)
    paginator = Paginator(players, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        own_player = PlayerDetails.objects.get(user=request.user)
    except PlayerDetails.DoesNotExist:
        own_player = None

    return TemplateResponse(request, 'medics/leaderboard.html', {
        'page_obj': page_obj,
        'own_player': own_player,
        'query': query
    })


@login_required
def add_colleague(request, player_details_id):
    tracker_details = get_object_or_404(PlayerDetails, user=request.user)
    colleague_details = get_object_or_404(PlayerDetails, id=player_details_id)
    if tracker_details.id == colleague_details.id:
        messages.warning(request, 'You cannot add yourself as a colleague!')
        return redirect('medics:leaderboard')
    _, created = ColleagueTracker.objects.get_or_create(
        tracker=tracker_details,
        tracked_colleague=colleague_details
    )
    if created:
        messages.success(
            request,
            f'Player {colleague_details.user.username} was added to your colleagues!'
        )
    else:
        messages.info(
            request,
            f'Player {colleague_details.user.username} is already in your colleagues!'
        )
    return redirect('medics:progress', user_id=request.user.id)


@login_required
def avatars(request):
    if request.method == 'POST':
        avatar_name = request.POST.get('avatar_name')
        if not avatar_name:
            raise Http404
        avatar = get_object_or_404(Avatar, name=avatar_name)
        details = get_object_or_404(PlayerDetails, user=request.user)
        details.avatar = avatar
        details.save()
        messages.success(request, 'Avatar changed successfully!')
        return redirect('medics:progress', user_id=request.user.id)
    if request.method == 'GET':
        return TemplateResponse(request, 'medics/avatars.html', {
            'avatars': Avatar.objects.all()
        })
    raise Http404
