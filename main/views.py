from django.shortcuts import render

from main.pokemon import Pokemon, InvalidLevelException, InvalidSpeciesException
from .forms import InputForm


def index(request):
    """Render Simple Page"""
    context = {}

    if request.method == 'GET':
        context['form'] = InputForm()
    elif request.method == 'POST':
        form = InputForm(request.POST)
        context['form'] = form

        if form.is_valid():
            species = form.cleaned_data['pokemon']
            level = int(form.cleaned_data['level'])

            try:
                pokemon = Pokemon(species, level)
            except InvalidLevelException:
                context['success'] = False
                context['error'] = 'bad-level'
                return render(request, 'main/index.html', context)
            except InvalidSpeciesException:
                context['success'] = False
                context['error'] = 'bad-species'
                return render(request, 'main/index.html', context)

            boosts = pokemon.generate_boosts()
            pokemon.apply_boosts(boosts)

            # data has species, level, stats, and moveset
            data = {
                'species': species,
                'level': level,
                'moves': pokemon.moveset,
                'image': pokemon.image,
            }
            data.update(pokemon.stats)

            # rename special stats to have underscore in place of dash
            data['special_attack'] = data.pop('special-attack')
            data['special_defense'] = data.pop('special-defense')

            context['success'] = True
            context['data'] = data

    return render(request, 'main/index.html', context)
