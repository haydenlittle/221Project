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

# def recurse(distnum_to_possible_adds, assigned_precincts, dist_to_num_people, num) :
#     for dist in dist_to_num_people :
#         if dist_to_num_people[dist] > 470000 :
#             return False
#     if len(assigned_precincts) == len(precincts) :
#         return True
#     for i in range(1, 9) :
#         for poss_add in distnum_to_possible_adds[i].copy() :
#             if poss_add in assigned_precincts.copy() :
#                 distnum_to_possible_adds[i].remove(poss_add)
#     for dist in distnum_to_possible_adds :
#         for next_add in distnum_to_possible_adds[dist] :
#             new_dist_to_num_people = copy.deepcopy(dist_to_num_people)
#             new_dist_to_num_people[dist] += (precincts[next_add]['num_registered_voters'])
#             new_assigned_precincts = copy.deepcopy(assigned_precincts)
#             new_assigned_precincts[next_add] = dist
#             if recurse(copy.deepcopy(distnum_to_possible_adds), new_assigned_precincts, new_dist_to_num_people, num + 1) :
#                 return

def noMovesLeft(dictionary) :
    for entry in dictionary :
        if len(dictionary[entry]) != 0:
            return False
    return True

# def recurse(distnum_to_possible_adds, assigned_precincts, dist_to_num_people, count) :
#     if dist_to_num_people[1] > 470000 :
#         count[0] += 1
#         if count[0] % 100 == 0 :
#             print count[0]
#         return
#     if len(assigned_precincts) == len(precincts) :
#         print 'fuck'
#         return True
#     for i in range(1, 9) :
#         for poss_add in distnum_to_possible_adds[i].copy() :
#             if poss_add in assigned_precincts.copy() :
#                 distnum_to_possible_adds[i].remove(poss_add)
#     for next_add in distnum_to_possible_adds[1] :
#         new_dist_to_num_people = copy.deepcopy(dist_to_num_people)
#         new_dist_to_num_people[1] += (precincts[next_add]['num_registered_voters'])
#         new_assigned_precincts = copy.deepcopy(assigned_precincts)
#         new_assigned_precincts[next_add] = 1
#         new_distnum_to_possible_adds = copy.deepcopy(distnum_to_possible_adds)
#         for n in precincts[next_add]['neighbors'] :
#             new_distnum_to_possible_adds[1].add(n)
#         recurse(new_distnum_to_possible_adds, new_assigned_precincts, new_dist_to_num_people, count)


best_ass_prec = ({}, 10000)

for iterat in range(0, 100) :
    print('iter ' + str(iterat))
    precincts = load_obj('precincts_with_voter_data')
    # for precinct in precincts :
    #     precincts[precinct]['district'] = 6
    #
    # for precinct in precincts :
    #     precincts[precinct]['district'] = random.randint(1, 8)
    #     if len(precincts[precinct]['neighbors']) == 1 :
    #         precincts[precinct]['district'] = 2
    #         precincts[precincts[precinct]['neighbors'].pop()]['district'] = 2

    distnum_to_possible_adds = {}
    #assigned_precincts = set()

    assigned_precincts = {}
    dist_to_num_people = {}
    dist_to_num_repubs = {}
    dist_to_num_dems = {}


    for precinct in precincts :
        precincts[precinct]['district'] = 9

    starting_precincts = random.sample(precincts, 9)
    for i in range(1, 9) :
        precincts[starting_precincts[i]]['district'] = i
        distnum_to_possible_adds[i] = copy.deepcopy(precincts[starting_precincts[i]]['neighbors'])
        dist_to_num_people[i] = 0
        dist_to_num_dems[i] = 0
        dist_to_num_repubs[i] = 0
        #assigned_precincts.add(starting_precincts[i])
        assigned_precincts[starting_precincts[i]] = i

    count = [0]
    possibilities = [n for n in range(1,9)]
    #recurse(distnum_to_possible_adds, assigned_precincts, dist_to_num_people, count)
    end = False
    while True :
        # for i in range(1, 9) :
        if len(possibilities) != 0 :
            x = min([(n, dist_to_num_people[n]) for n in possibilities], key=lambda x:x[1])
            i = x[0]
        else :
            break
        if len(distnum_to_possible_adds[i]) == 0 :
            print('no moves left for ' + str(i))
            possibilities.remove(i)
            continue
        if len(possibilities) == 0 :
            print 'sucks'
            end = True
            break
        # if dist_to_num_people[i] > 480000 :
        #     possibilities.remove(i)
        #     print('overage for' + str(i))
        #     continue
        if len(precincts) == len(assigned_precincts) :
            end = True
            break
        if len(distnum_to_possible_adds[i]) == 0 :
            continue
        for poss_add in distnum_to_possible_adds[i].copy() :
            if poss_add in assigned_precincts.copy() :
                distnum_to_possible_adds[i].remove(poss_add)
        # next_add = random.sample(distnum_to_possible_adds[i], 1)[0]
        best_candidate = ('0', 0)
        for candid in distnum_to_possible_adds[i] :
            if dist_to_num_people[i] + precincts[candid]['num_registered_voters'] == 0:
                continue
            perc_dem = float(dist_to_num_dems[i] + precincts[candid]['num_democratic_votes']) / float(dist_to_num_people[i] + precincts[candid]['num_registered_voters'])
            if abs(perc_dem - 50.0) < abs(list(best_candidate)[1] - 50.0) :
                best_candidate = (candid, abs(perc_dem - 50.0))
        next_add = list(best_candidate)[0]
        distnum_to_possible_adds[i].remove(next_add)
        for dist in distnum_to_possible_adds :
            if next_add in distnum_to_possible_adds[dist] :
                distnum_to_possible_adds[dist].remove(next_add)
        precincts[next_add]['district'] = i
        assigned_precincts[next_add] = i
        dist_to_num_people[i] += precincts[next_add]['num_registered_voters']
        dist_to_num_dems[i] += precincts[next_add]['num_democratic_votes']
        dist_to_num_repubs[i] += precincts[next_add]['num_republican_votes']
        for neighbor in precincts[next_add]['neighbors'] :
            if neighbor not in assigned_precincts :
                distnum_to_possible_adds[i].add(neighbor)
        if end :
            break

# print best_ass_prec[1]

    for i in range(1, 9) :
        print (float(dist_to_num_repubs[i]) / float(dist_to_num_people[i]), dist_to_num_people[i])

    if (sum([abs(float(dist_to_num_repubs[i]) / float(dist_to_num_people[i])) - 50.0 for i in range(1,9)]) < list(best_ass_prec)[1]):
        best_ass_prec = (assigned_precincts.copy(), sum([abs(float(dist_to_num_repubs[i]) / float(dist_to_num_people[i])) - 50.0 for i in range(1,9)]))

json_data = open('mn-precincts.json')
data = json.load(json_data)
for entry in data['features'] :
    # entry['properties']['CongDist'] = precincts[entry['properties']['PrecinctID']]['district']
    if entry['properties']['PrecinctID'] in list(best_ass_prec)[0] :
        entry['properties']['CongDist'] = list(best_ass_prec)[0][entry['properties']['PrecinctID']]
    else :
        entry['properties']['CongDist'] = 9
# for i in range(0, len(data['features'])) :
#     data['features'][i]['properties']['Cong']

with open('cong-assignments.json', 'w') as outfile :
    json.dump(data, outfile)
