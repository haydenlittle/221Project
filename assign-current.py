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

def get_score(people, repubs) :
    score = 0
    for i in range(1, 9) :
        if i != 5 :
            assignment = (float(repubs[i]) / float(people[i]), people[i])

            assignment5 = (float(repubs[5]) / float(people[5]), people[5])
            if assignment[0] < 0.5 :
                score += (1 + 0.5 - assignment[0])
            if assignment[1] < 400000 or assignment[1] > 500000 or assignment5[1] < 400000 or assignment5[1] > 500000:
                score = float('inf')
                break
    return score

def neighborInSameDistrict(precincts, precinct) :
    # dist = precincts[precinct]['district']
    for neighbor in precincts[precinct]['neighbors'] :
        Pass = False
        for inner_neighbor in precincts[neighbor]['neighbors'] :
            if precincts[neighbor]['district'] == precincts[inner_neighbor]['district'] and inner_neighbor != precinct:
                Pass = True
        if not Pass :
            return False
    return True

def allFound(found) :
    for item in found :
        if item[1] == False :
            return False
    return True

def DFS(curr, found, explored, precincts) :
    explored.add(curr)
    if (curr, False) in found :
        found.remove((curr, False))
        found.add((curr, True))
        print 'FOUND'
    if allFound(found) :
        return True
    for neighbor in precincts[curr]['neighbors'] :
        if neighbor not in explored :
            if DFS(neighbor, found, explored, precincts) :
                return True
    return False

def validMove(precincts, precinct) :
    neighbors = precincts[precinct]['neighbors']
    testers = set()
    for neighbor in neighbors :
        if precincts[neighbor]['district'] == precincts[precinct]['district'] and len(precincts[neighbor]['neighbors']) != 1 :
            testers.add(neighbor)
    for tester in testers :
        explored = set()
        found = set()
        for in_tester in testers :
            if in_tester != tester :
                found.add((in_tester, False))
        if not DFS(tester, found, explored, precincts) :
            return False
    return True

def validState(precincts) :
    for precinct in precincts :
        if not neighborInSameDistrict(precincts, precinct) :
            return False
    return True

def onlyNeighbor(precincts, precinct, neighbor, wantprint = False) :
    dists = set()
    for neighbor in precincts[precinct]['neighbors'] :
        dists.add(precincts[neighbor]['district'])
    if wantprint :
        print dists
    if len(dists) != 2 :
        return False
    else :
        # dists = set()
        # for neighbor in precincts[neighbor]['neighbors'] :
        #     dists.add(precincts[neighbor]['district'])
        # if len(dists) != 2 :
        #     return False
        # else :
        #     return True
        return True

def get_actions(state) :
    actions = set()
    for precinct in state :
        for neighbor in precincts[precinct]['neighbors'] :
            if precincts[neighbor]['district'] != precincts[precinct]['district'] and onlyNeighbor(precincts, neighbor, precinct) and neighborInSameDistrict(precincts, neighbor) and len(precincts[precinct]['points'] & precincts[neighbor]['points']) > 1:

                # actions.add('SWAP PRECINCTS ' + str(precinct) + ' AND ' + str(neighbor) + 'FROM DISTRICTS ' + str(precincts[precinct]['district']) + ' AND ' + str(precincts[neighbor]['district']))
                actions.add((neighbor, precincts[precinct]['district']))
    #             switcher.add((precincts[neighbor]['district'], precincts[precinct]['district']))
    # for switch in switcher :
    #     print switch
    return actions


def updateLoneNeighbors(precincts) :
    for precinct in precincts :
        if len(precincts[precinct]['neighbors']) == 1 :
            precincts[precinct]['district'] = precincts[list(precincts[precinct]['neighbors'])[0]]['district']


precincts = load_obj('precincts_with_voter_data')

dist_to_num_people = {}
dist_to_num_dems = {}
dist_to_num_repubs = {}

for i in range(1, 9) :
    dist_to_num_people[i] = 0
    dist_to_num_dems[i] = 0
    dist_to_num_repubs[i] = 0

json_data = open('mn-precincts.json')
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

old_score = get_score(dist_to_num_people, dist_to_num_repubs)

learned_weight = 100
step = 1
weights = []

best_assignment = (False, float('inf'))

for j in range(0, 10) :
    print('ITERATION ' + str(j) + '/10')
    for i in range(0, 500) :
        # print i
        actions = get_actions(precincts)
        # print len(actions)
        scores = []
        for action in actions :
            old_dist = int(precincts[action[0]]['district'])
            new_dist = int(action[1])
            dist_to_num_repubs[old_dist] -= precincts[action[0]]['num_republican_votes']
            dist_to_num_people[old_dist] -= precincts[action[0]]['num_registered_voters']
            dist_to_num_repubs[new_dist] += precincts[action[0]]['num_republican_votes']
            dist_to_num_people[new_dist] += precincts[action[0]]['num_registered_voters']
            new_score = (action, get_score(dist_to_num_people, dist_to_num_repubs))
            scores.append(new_score)
            dist_to_num_repubs[old_dist] += precincts[action[0]]['num_republican_votes']
            dist_to_num_people[old_dist] += precincts[action[0]]['num_registered_voters']
            dist_to_num_repubs[new_dist] -= precincts[action[0]]['num_republican_votes']
            dist_to_num_people[new_dist] -= precincts[action[0]]['num_registered_voters']

        # print('OLD DIST: ' + str(old_dist))
        # print('NEW DIST: ' + str(new_dist))
        new_action = min(scores, key=lambda x:x[1])
        # print('NEW ACTION: ' + str(new_action))
        # print new_action[1]
        # print new_action
        prob = 1.0 / (1 + math.exp( new_action[1] * learned_weight - old_score * learned_weight))
        # print prob
        # print prob
        randy = random.random()
        # print randy
        if prob < randy :
            old_dist = int(precincts[new_action[0][0]]['district'])
            new_dist = int(new_action[0][1])
            dist_to_num_repubs[old_dist] -= precincts[new_action[0][0]]['num_republican_votes']
            dist_to_num_people[old_dist] -= precincts[new_action[0][0]]['num_registered_voters']
            dist_to_num_repubs[new_dist] += precincts[new_action[0][0]]['num_republican_votes']
            dist_to_num_people[new_dist] += precincts[new_action[0][0]]['num_registered_voters']
            precincts[new_action[0][0]]['district'] = new_dist
            old_score = new_action[1]
            updateLoneNeighbors(precincts)
            # onlyNeighbor(precincts, new_action[0][0], new_action[0][0], True)
        else :
            rip = float('inf')
            while rip == float('inf') :
                new_action = random.sample(scores, 1)[0]
                rip = new_action[1]
            # print new_action
            # print new_action
            old_dist = int(precincts[new_action[0][0]]['district'])
            new_dist = int(new_action[0][1])
            dist_to_num_repubs[old_dist] -= precincts[new_action[0][0]]['num_republican_votes']
            dist_to_num_people[old_dist] -= precincts[new_action[0][0]]['num_democratic_votes']
            dist_to_num_repubs[new_dist] += precincts[new_action[0][0]]['num_republican_votes']
            dist_to_num_people[new_dist] += precincts[new_action[0][0]]['num_republican_votes']
            precincts[new_action[0][0]]['district'] = new_dist
            updateLoneNeighbors(precincts)
            old_score = new_action[1]
            # print new_action[1]

        if old_score < best_assignment[1] :
            best_assignment = (precincts, old_score)
            print('new best assignment found with score: ' + str(best_assignment[1]))
            for i in range(1, 9) :
                assignment = (float(dist_to_num_repubs[i]) / float(dist_to_num_people[i]), dist_to_num_people[i])
                print assignment



    for i in range(1, 9) :
        assignment = (float(dist_to_num_repubs[i]) / float(dist_to_num_people[i]), dist_to_num_people[i])
        # print assignment
    if i == 0 :
        weights.append((learned_weight, get_score(dist_to_num_people, dist_to_num_repubs)))
        learned_weight = 101
    else :
        weights.append((learned_weight, get_score(dist_to_num_people, dist_to_num_repubs)))
        score_delta = weights[len(weights) - 1][1] - weights[len(weights) - 2][1]
        learned_weight -= score_delta * step
    print learned_weight


for entry in data['features'] :
    entry['properties']['CongDist'] = best_assignment[0][entry['properties']['PrecinctID']]['district']

with open('cong-assignments.json', 'w') as outfile :
    json.dump(data, outfile)
