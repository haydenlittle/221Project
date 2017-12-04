import json
import pickle
import math
import csv
import copy
import codecs
from ast import literal_eval as make_tuple

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


# precincts = {}
# old_precincts = load_obj('precincts')
# json_data = open('mn-precincts.json')
# data = json.load(json_data)
# for entry in data['features'] :
    # print entry['properties']['Precinct']
    # precincts[entry['properties']['Precinct']] = {}
    # precincts[entry['properties']['Precinct']]['points'] = set()
    # precincts[entry['properties']['Precinct']]['neighbors'] = set()
    # precincts[entry['properties']['PrecinctID']] = {}
    # precincts[entry['properties']['PrecinctID']]['name'] = entry['properties']['Precinct']
    # precincts[entry['properties']['PrecinctID']]['points'] = set()
    # precincts[entry['properties']['PrecinctID']]['neighbors'] = copy.deepcopy(old_precincts[entry['properties']['Precinct']]['neighbors'])
#     precincts[entry['properties']['PrecinctID']]['neighbors'] = set()
#     for x in entry['geometry']['coordinates'] :
#         for y in x :
#             if len(y) != 2 :
#                 for z in y :
#                     precincts[entry['properties']['PrecinctID']]['points'].add(tuple(z))
#             else :
#                 precincts[entry['properties']['PrecinctID']]['points'].add(tuple(y))
# count = 1
# for precinct1 in precincts :
#     print('executing precinct ' + str(count) + ' out of ' + str(len(precincts)))
#     for precinct2 in precincts :
#         if precinct1 != precinct2 :
#             if any(i in precincts[precinct1]['points'] for i in precincts[precinct2]['points']) :
#                 precincts[precinct1]['neighbors'].add(precinct2)
#     if len(precincts[precinct1]['neighbors']) == 0 :
#         print('no neighbors found for ' + precinct1)
#     count += 1
# save_obj(precincts, 'precincts')

# precincts['270010150']['neighbors'].add('270010110')
# precincts['270010110']['neighbors'].add('270010150')
# precincts['271170115']['neighbors'].add('271170030')
# precincts['271170030']['neighbors'].add('271170115')
# precincts['271010075']['neighbors'].add('271530100')
# precincts['271530100']['neighbors'].add('271010075')
# precincts['270290015']['neighbors'].add('270290075')
# precincts['270290075']['neighbors'].add('270290015')
# precincts['270010190']['neighbors'].add('270430040')
# precincts['270430040']['neighbors'].add('270010190')
# precincts['270450185']['neighbors'].add('270890120')
# precincts['270890120']['neighbors'].add('270450185')
# precincts['270350105']['neighbors'].add('270350110')
# precincts['270350110']['neighbors'].add('270350105')
# precincts['270110040']['neighbors'].add('271670005')
# precincts['271670005']['neighbors'].add('270110040')
# precincts['271330110']['neighbors'].add('271370115')
# precincts['271370115']['neighbors'].add('271330110')
# precincts['270290045']['neighbors'].add('270290100')
# precincts['270290100']['neighbors'].add('270290045')
# precincts['271170060']['neighbors'].add('271190160')
# precincts['271190160']['neighbors'].add('271170060')

# precincts = load_obj('precincts')

precincts = load_obj('precincts')

# for precinct in precincts :
#     if len(precincts[precinct]['neighbors']) == 0 :
#         print('no neighbors found for ' + precinct)
# save_obj(precincts, 'precincts')


# old_precincts = load_obj('precincts')
# for pid in precincts :
#     precincts['neighbors'] = copy.deepcopy(old_precincts[precincts[pid]['name']]['neighbors'])

id_to_numvoters = {}
id_to_republican_votes = {}
id_to_democratic_votes = {}

with codecs.open('electionresults.csv', 'rU', encoding="utf-8-sig") as voteCounts:
    reader = csv.DictReader(voteCounts, )
    for row in reader :
        # print(make_tuple(row['ID_NAME_PAIR']), int(row['NUM_REGISTERED_VOTERS']))
        # print(row['PCTNAME'], int(row['REG7AM']) + int(row['EDR']))
        #precincts[row['VTDID']]['num_registered_voters'] = int(row['REG7AM']) + int(row['EDR'])
        id_to_numvoters[row['VTDID']] = int(row['REG7AM']) + int(row['EDR'])
        if row['USPRSR'] == '0' and row['USPRSDFL'] == '0' :
            id_to_republican_votes[row['VTDID']] = 0
            id_to_democratic_votes[row['VTDID']] = 0
        elif row['USPRSR'] != '0' and row['USPRSDFL'] == '0' :
            id_to_democratic_votes[row['VTDID']] = 0
            id_to_republican_votes[row['VTDID']] = int(row['REG7AM']) + int(row['EDR'])
        elif row['USPRSR'] == '0' and row['USPRSDFL'] != '0' :
            id_to_democratic_votes[row['VTDID']] = int(row['REG7AM']) + int(row['EDR'])
            id_to_republican_votes[row['VTDID']] = 0
        else :
            id_to_republican_votes[row['VTDID']] = int((float(row['USPRSR']) / (int(row['USPRSR']) + int(row['USPRSDFL']))) * (int(row['REG7AM']) + int(row['EDR'])))
            id_to_democratic_votes[row['VTDID']] = int(row['REG7AM']) + int(row['EDR']) - id_to_republican_votes[row['VTDID']]
        # print row.keys()

for precinct in precincts :
    if precinct in id_to_numvoters :
        precincts[precinct]['num_registered_voters'] = id_to_numvoters[precinct]
        precincts[precinct]['num_republican_votes'] = id_to_republican_votes[precinct]
        precincts[precinct]['num_democratic_votes'] = id_to_democratic_votes[precinct]
    else :
        precincts[precinct]['num_registered_voters'] = 0
        precincts[precinct]['num_republican_votes'] = 0
        precincts[precinct]['num_democratic_votes'] = 0

save_obj(precincts, 'precincts_with_voter_data')


# precinct1 = precincts['Freedom Twp']
# precinct2 = precincts['Wilton Twp']
# if any(i in precinct1['points'] for i in precinct2['points']) :
#     print 'suck my dick'
