import json
import pickle
import math

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

# precincts = {}
# json_data = open('mn-precincts.json')
# data = json.load(json_data)
# for entry in data['features'] :
#     # print entry['properties']['Precinct']
#     precincts[entry['properties']['Precinct']] = {}
#     precincts[entry['properties']['Precinct']]['points'] = set()
#     precincts[entry['properties']['Precinct']]['neighbors'] = set()
#     for x in entry['geometry']['coordinates'] :
#         for y in x :
#             if len(y) != 2 :
#                 for z in y :
#                     precincts[entry['properties']['Precinct']]['points'].add(tuple(z))
#             else :
#                 precincts[entry['properties']['Precinct']]['points'].add(tuple(y))
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

# precincts = load_obj('precincts')
# precincts['Palisade']['neighbors'].add('Logan Twp')
# precincts['Logan Twp']['neighbors'].add('Palisade')
# precincts['Trosky']['neighbors'].add('Elmer Twp')
# precincts['Elmer Twp']['neighbors'].add('Trosky')
# precincts['Iona']['neighbors'].add('Iona Twp')
# precincts['Iona Twp']['neighbors'].add('Iona')
# precincts['Clearbrook']['neighbors'].add('Leon Twp')
# precincts['Leon Twp']['neighbors'].add('Clearbrook')
# precincts['Tamarack']['neighbors'].add('Clark Twp')
# precincts['Clark Twp']['neighbors'].add('Tamarack')
# precincts['Whalan']['neighbors'].add('Holt Twp')
# precincts['Holt Twp']['neighbors'].add('Whalan')
# precincts['Deerwood']['neighbors'].add('Deerwood Twp')
# precincts['Deerwood Twp']['neighbors'].add('Deerwood')
# precincts['Correll']['neighbors'].add('Akron Twp')
# precincts['Akron Twp']['neighbors'].add('Correll')
# precincts['Steen']['neighbors'].add('Clinton Twp')
# precincts['Clinton Twp']['neighbors'].add('Steen')
# precincts['Gonvick']['neighbors'].add('Pine Lake Twp')
# precincts['Pine Lake Twp']['neighbors'].add('Gonvick')
# precincts['Ihlen']['neighbors'].add('Eden Twp')
# precincts['Eden Twp']['neighbors'].add('Ihlen')

precincts = load_obj('precincts')
for precinct in precincts :
    if len(precincts[precinct]['neighbors']) == 0 :
        print('no neighbors found for ' + precinct)
# save_obj(precincts, 'precincts')

# precinct1 = precincts['Freedom Twp']
# precinct2 = precincts['Wilton Twp']
# if any(i in precinct1['points'] for i in precinct2['points']) :
#     print 'suck my dick'
