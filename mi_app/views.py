import random

from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import PlayerForm
from .models import Match, Player, TeamAssignment, TierEntry


def index(request):
    players = Player.objects.all().order_by('nombre')
    error = None

    if request.method == 'POST':
        if 'match_submit' in request.POST:
            formato = request.POST.get('formato')
            equipo1_color = request.POST.get('equipo1_color') or 'blanco'
            equipo2_color = request.POST.get('equipo2_color') or 'negro'
            selected_ids = request.POST.getlist('jugadores')

            if formato is None or formato == '':
                error = 'Debes seleccionar un formato de partido.'
            else:
                match = Match.objects.create(
                    formato=formato,
                    equipo1_color=equipo1_color,
                    equipo2_color=equipo2_color,
                )
                selected_players = list(Player.objects.filter(id__in=selected_ids))
                required = match.get_required_player_count()
                if len(selected_players) < required:
                    match.delete()
                    error = f'Se necesitan {required} jugadores para un partido {formato}. Has seleccionado {len(selected_players)}.'
                else:
                    chosen_players = random.sample(selected_players, required)
                    match.jugadores.set(chosen_players)
                    return redirect(reverse('sorteo') + f'?match_id={match.id}')

    return render(request, 'mi_app/index.html', {
        'players': players,
        'error': error,
    })


def add_player(request):
    player_form = PlayerForm()
    if request.method == 'POST':
        player_form = PlayerForm(request.POST, request.FILES)
        if player_form.is_valid():
            player_form.save()
            return redirect('index')

    return render(request, 'mi_app/add_player.html', {
        'player_form': player_form,
    })


def delete_player(request, player_id):
    try:
        player = Player.objects.get(pk=player_id)
        player.delete()
    except Player.DoesNotExist:
        pass
    return redirect('index')


def sorteo(request):
    match_id = request.GET.get('match_id') or request.POST.get('match_id')
    match = None
    error = None
    assignments = []

    if match_id:
        try:
            match = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            error = 'Partido no encontrado.'
    else:
        error = 'No se ha seleccionado un partido para sortear.'

    if match:
        assignments = list(match.asignaciones.select_related('player'))
        if not assignments:
            players = list(match.jugadores.all())
            random.shuffle(players)
            half = len(players) // 2
            for player in players[:half]:
                assignments.append(TeamAssignment.objects.create(match=match, player=player, team=1))
            for player in players[half:]:
                assignments.append(TeamAssignment.objects.create(match=match, player=player, team=2))

        team1 = [assignment.player for assignment in assignments if assignment.team == 1]
        team2 = [assignment.player for assignment in assignments if assignment.team == 2]
    else:
        team1 = []
        team2 = []

    return render(request, 'mi_app/sorteo.html', {
        'match': match,
        'team1': team1,
        'team2': team2,
        'error': error,
    })


def tier_list(request):
    matches = Match.objects.order_by('-fecha')
    selected_match_id = request.GET.get('match_id') or request.POST.get('match_id')
    selected_match = None
    entries = {}
    message = None

    if selected_match_id:
        try:
            selected_match = Match.objects.get(pk=selected_match_id)
        except Match.DoesNotExist:
            selected_match = None

    if request.method == 'POST' and selected_match:
        for player in selected_match.jugadores.all():
            field_name = f'category_{player.id}'
            category = request.POST.get(field_name)
            if category:
                entry, _ = TierEntry.objects.get_or_create(player=player, match=selected_match)
                entry.category = category
                entry.save()
        message = 'Tier list actualizada correctamente.'

    player_entries = []
    if selected_match:
        for player in selected_match.jugadores.all():
            entry, _ = TierEntry.objects.get_or_create(player=player, match=selected_match)
            player_entries.append({
                'player': player,
                'category': entry.category,
            })

    return render(request, 'mi_app/tier_list.html', {
        'matches': matches,
        'selected_match': selected_match,
        'player_entries': player_entries,
        'message': message,
    })
