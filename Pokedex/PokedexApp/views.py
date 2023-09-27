from django.shortcuts import render
import urllib.request
import json
from http import HTTPStatus
from urllib.error import HTTPError

def index(request):
    try:
        if request.method == 'POST':
            pokemon = request.POST['pokemon'].lower()
            pokemon = pokemon.replace(' ', '%20')
            url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{pokemon}/')
            url_pokeapi.add_header('User-Agent', 'charmander')

            source = urllib.request.urlopen(url_pokeapi).read()

            list_of_data = json.loads(source)

            # convertendo a altura para metro
            height_obtained = (float(list_of_data['height'] * 0.1))
            height_obtained = round(height_obtained, 2)

            # convertendo o peso para kilogramas
            weight_obtained = (float(list_of_data['weight'] * 0.1))
            weight_obtained = round(weight_obtained, 2)

            data = {
                "number": str(list_of_data['id']),
                "name": str(list_of_data['name']).capitalize(),

                "type1": str(list_of_data['types']),

                "height": str(height_obtained) + 'm',
                "weight": str(weight_obtained) + 'Kg',
                "sprite": str(list_of_data['sprites']['front_default']),
            }

        else:
            data = {}

        return render(request, 'main/index.html', data)
    except HTTPError as e:
        if e.code == 404:
            return render(request, 'main/404.html')