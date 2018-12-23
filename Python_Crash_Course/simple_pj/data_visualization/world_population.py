import json
import pygal
from pygal_maps_world.i18n import COUNTRIES
from pygal_maps_world.maps import World
from pygal.style import LightColorizedStyle, RotateStyle


def code_find(countryname):
    for country_code in COUNTRIES.keys():
        if(countryname == COUNTRIES[country_code]):
            return country_code
        elif(COUNTRIES[country_code] in countryname):
            return country_code
    return None


file_name = "population_data.json"

with open(file_name) as f:
    data = json.load(f)
    pop_1, pop_2, pop_3 = {}, {}, {}
    for item in data:
        if item['Year'] == '2010':
            country_name = item['Country Name']
            population = int(float(item['Value']))
            code = code_find(country_name)
            if code:
                if population < 10000000:
                    pop_1[code] = population
                elif population < 1000000000:
                    pop_2[code] = population
                else:
                    pop_3[code] = population

print(len(pop_1), len(pop_2), len(pop_3))
wm = World()
wm_style = RotateStyle('#336699', base_style=LightColorizedStyle)
wm = World(style=wm_style)
wm.title = 'World Population in 2010, by Country'
wm.add('0-10M', pop_1)
wm.add('10M-1bn', pop_2)
wm.add('>1bn', pop_3)

wm.render_to_file('World_Population_2010.svg')