import pickle
import random
import json
import copy
import math

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

precincts = load_obj('precincts_with_voter_data')

dist_to_num_people = {}
dist_to_num_dems = {}
dist_to_num_repubs = {}

for i in range(1, 9) :
    dist_to_num_people[i] = 0
    dist_to_num_dems[i] = 0
    dist_to_num_repubs[i] = 0

json_data = open('cong-assignments.json')
data = json.load(json_data)
# for entry in data['features'] :
    # entry['properties']['CongDist'] = precincts[entry['properties']['PrecinctID']]['district']
    # if entry['properties']['PrecinctID'] in list(best_ass_prec)[0] :
    #     entry['properties']['CongDist'] = list(best_ass_prec)[0][entry['properties']['PrecinctID']]
    # else :
    #     entry['properties']['CongDist'] = 9

for entry in data['features'] :
    precincts[entry['properties']['PrecinctID']]['district'] = int(entry['properties']['CongDist'])
    dist_to_num_people[int(entry['properties']['CongDist'])] += precincts[entry['properties']['PrecinctID']]['num_registered_voters']
    dist_to_num_dems[int(entry['properties']['CongDist'])] += precincts[entry['properties']['PrecinctID']]['num_democratic_votes']
    dist_to_num_repubs[int(entry['properties']['CongDist'])] += precincts[entry['properties']['PrecinctID']]['num_republican_votes']

for i in range(1, 9) :
    assignment = (float(dist_to_num_repubs[i]) / float(dist_to_num_people[i]), dist_to_num_people[i])
    print assignment
