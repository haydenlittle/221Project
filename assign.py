import pickle
import random
import json

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

precincts = load_obj('precincts_with_voter_data')

for precinct in precincts :
    precincts[precinct]['district'] = 6

for precinct in precincts :
    precincts[precinct]['district'] = random.randint(1, 8)
    # if len(precincts[precinct]['neighbors']) == 1 :
    #     precincts[precinct]['district'] = 2
    #     precincts[precincts[precinct]['neighbors'].pop()]['district'] = 2


json_data = open('mn-precincts.json')
data = json.load(json_data)
for entry in data['features'] :
    entry['properties']['CongDist'] = precincts[entry['properties']['PrecinctID']]['district']
# for i in range(0, len(data['features'])) :
#     data['features'][i]['properties']['Cong']

with open('cong-assignments.json', 'w') as outfile :
    json.dump(data, outfile)
