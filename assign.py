import pickle
import random
import json
import copy

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def recurse(distnum_to_possible_adds, assigned_precincts, dist_to_num_people, num) :
    if num % 10 == 0 :
        print num
    for dist in dist_to_num_people :
        if dist_to_num_people[dist] > 470000 :
            return False
    if len(assigned_precincts) == len(precincts) :
        return True
    for i in range(1, 9) :
        for poss_add in distnum_to_possible_adds[i].copy() :
            if poss_add in assigned_precincts.copy() :
                distnum_to_possible_adds[i].remove(poss_add)
    for dist in distnum_to_possible_adds :
        for next_add in distnum_to_possible_adds[dist] :
            new_dist_to_num_people = copy.deepcopy(dist_to_num_people)
            new_dist_to_num_people[dist] += (precincts[next_add]['num_registered_voters'])
            new_assigned_precincts = copy.deepcopy(assigned_precincts)
            new_assigned_precincts[next_add] = dist
            if recurse(copy.deepcopy(distnum_to_possible_adds), new_assigned_precincts, new_dist_to_num_people, num + 1) :
                return


precincts = load_obj('precincts_with_voter_data')

# for precinct in precincts :
#     precincts[precinct]['district'] = 6
#
# for precinct in precincts :
#     precincts[precinct]['district'] = random.randint(1, 8)
    # if len(precincts[precinct]['neighbors']) == 1 :
    #     precincts[precinct]['district'] = 2
    #     precincts[precincts[precinct]['neighbors'].pop()]['district'] = 2

distnum_to_possible_adds = {}
#assigned_precincts = set()

assigned_precincts = {}
dist_to_num_people = {}


for precinct in precincts :
    precincts[precinct]['district'] = 9

starting_precincts = random.sample(precincts, 9)
for i in range(1, 9) :
    precincts[starting_precincts[i]]['district'] = i
    distnum_to_possible_adds[i] = copy.deepcopy(precincts[starting_precincts[i]]['neighbors'])
    dist_to_num_people[i] = 0
    #assigned_precincts.add(starting_precincts[i])
    assigned_precincts[starting_precincts[i]] = i

recurse(distnum_to_possible_adds, assigned_precincts, dist_to_num_people, 0)

# end = False
# while True :
#     for i in range(1, 9) :
#         if len(precincts) == len(assigned_precincts) :
#             end = True
#             break
#         if len(distnum_to_possible_adds[i]) == 0 :
#             continue
        # for poss_add in distnum_to_possible_adds[i] :
        #     if poss_add in assigned_precincts :
        #         distnum_to_possible_adds[i].remove(poss_add)
#         next_add = random.sample(distnum_to_possible_adds[i], 1)[0]
#         distnum_to_possible_adds[i].remove(next_add)
#         for dist in distnum_to_possible_adds :
#             if next_add in distnum_to_possible_adds[dist] :
#                 distnum_to_possible_adds[dist].remove(next_add)
#         precincts[next_add]['district'] = i
#         assigned_precincts.add(next_add)
#         for neighbor in precincts[next_add]['neighbors'] :
#             if neighbor not in assigned_precincts :
#                 distnum_to_possible_adds[i].add(neighbor)
#     if end :
#         break


json_data = open('mn-precincts.json')
data = json.load(json_data)
for entry in data['features'] :
    entry['properties']['CongDist'] = precincts[entry['properties']['PrecinctID']]['district']
# for i in range(0, len(data['features'])) :
#     data['features'][i]['properties']['Cong']

with open('cong-assignments.json', 'w') as outfile :
    json.dump(data, outfile)
