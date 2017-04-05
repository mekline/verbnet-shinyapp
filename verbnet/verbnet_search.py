import cPickle as pickle
import cgi
import json

classes_dict = pickle.load(open('save.p','rb'))

def class_to_verbs(class_name):
	'''given the verb class, this function prints all the members in the main verb class and associated subclasses'''
	d = {}
	for x in classes_dict:
		my_list = [(k, v) for (k, v) in x.iteritems()]
		if class_name in k:
			my_list = my_list[0]
			verb_list = (my_list[1][0]['members'])
			verb_list = " ".join(verb_list)
			verb_list = verb_list.replace(" ", ", ")
			d[my_list[0]] = verb_list
			return(d)

def gen_dict_extract(key, var):
	''''This function extracts whatever keys out of the dictionaries'''
	if hasattr(var,'iteritems'):
		for k, v in var.iteritems():
			if k == key:
				yield v
			if isinstance(v, dict):
				for result in gen_dict_extract(key, v):
					yield result
			elif isinstance(v, list):
				for d in v:
					for result in gen_dict_extract(key, d):
						yield result

def frames_given_verb(search_verb,d_list=classes_dict):
	'''given a verb, prints frames for that verb'''
	frame_list = []
	if '_class_' in search_verb:
		search_verb = search_verb.split('_class_')
		search_class = search_verb[-1]
		for x in classes_dict:
			for keys in x:
				if search_class in keys:
					correct_class = x
	else:
		for x in classes_dict:
			my_list = [(k, v) for (k, v) in x.iteritems()]
			verbs_list=my_list[0][1][0]['members']
			verbs_list = " ".join(verbs_list)	
			verbs_list = verbs_list.replace(" ", ", ")
			verbs_list = verbs_list.split(", ")
			for i,v in enumerate(verbs_list):
				if '.' in v:
					v = v.split('.')
					v = v[0]
					verbs_list[i] = v
			if search_verb in verbs_list:
				correct_class = x
	frame = gen_dict_extract('frames', correct_class)
	frame = list(frame)
	iterframe = iter(frame)
	next(iterframe)
	for f in iterframe:
		frame_list.append(f['frame'])
	frame_list=list(set(frame_list))
	return(frame_list)

# def arg_given_verb(search_verb,d_list=classes_dict):
# 	'''given a verb, prints frames for that verb'''
# 	if '.' in search_verb:
# 		search_verb = search_verb.split('.')
# 		search_verb = search_verb[0]
# 	for x in d_list:
# 		my_list = [(k, v) for (k, v) in x.iteritems()]
# 		verbs_list=my_list[0][1][0]['members']
# 		verbs_list = " ".join(verbs_list)
# 		verbs_list = verbs_list.replace(" ", ", ")
# 		verbs_list = verbs_list.split(", ")
# 		for i,v in enumerate(verbs_list):
# 			if '.' in v:
# 				v = v.split('.')
# 				v = v[0]
# 				verbs_list[i] = v
# 		if any(search_verb in s for s in verbs_list):
# 			arguments = []				
# 			key = x.keys() 
# 			key = key[0]
# 			x = x[key]
# 			x = x[-1]
# 			x = x['frames']
# 			for frame in x:
# 				argument = frame['frames']['frame']
# 				if argument != '':
# 					arguments.append(argument)
# 			print('These frames take arguments for this verb:')
# 			print(arguments)

def agent_given_verb(search_verb,search_role,d_list=classes_dict):
	'''given a verb, answer Does it take an agent?'''
	if '_class_' in search_verb:
		search_verb = search_verb.split('_class_')
		search_class = search_verb[-1]
		for x in d_list:
			for keys in x:
				if search_class in keys:
					correct_class = x
	else:
		for x in d_list:
			my_list = [(k, v) for (k, v) in x.iteritems()]
			verbs_list=my_list[0][1][0]['members']
			verbs_list = " ".join(verbs_list)	
			verbs_list = verbs_list.replace(" ", ", ")
			verbs_list = verbs_list.split(", ")
			for i,v in enumerate(verbs_list):
				if '.' in v:
					v = v.split('.')
					v = v[0]
					verbs_list[i] = v
			if search_verb in verbs_list:
				correct_class = x
 	key = correct_class.keys() 
 	key = key[0]
 	correct_class = correct_class[key]
 	correct_class = correct_class[1]
 	correct_class = correct_class['themroles']
 	if search_role in correct_class:
 		return('Yes, this verb takes %ss.' %search_role)
 	else:
 		return('No, this verb does not take %ss.' %search_role)

# create a list of all the possible verb classes
class_list = []
for x in classes_dict:
	my_list = [(k, v) for (k, v) in x.iteritems()]
	verb_class = my_list[0][0]
	class_list.append(verb_class)

#creating list of all verbs
all_verbs = []
for x in classes_dict:
	for keys in x:
		if '-' in keys:
			class_verb = keys
	my_list = [(k, v) for (k, v) in x.iteritems()]
	verb_list=my_list[0][1][0]['members']
	verb_list = " ".join(verb_list)
	verb_list = verb_list.replace(" ", ", ")
	verb_list = verb_list.split(", ")
	for i, s in enumerate(verb_list):
		if '.0' in s:
			s = s.split('.')
			s = s[0]
			s += '_class_'
			s += str(class_verb)
			verb_list[i] = s
	all_verbs.append(verb_list)
all_verbs = [item for sublist in all_verbs for item in sublist] #flattening list
all_verbs = list(set(all_verbs)) #making this a list of unique verbs (removing duplicates)
all_verbs = list(filter(None, all_verbs)) #removing empty strings

#create list of all roles
all_roles = []
for x in classes_dict:
	x = gen_dict_extract('ThemRole', x)
	x = list(x)
	for i, v in enumerate(x):
		if type(v) == dict:
			x[i] = v.keys()
	all_roles.append(x)
all_roles = [item for sublist in all_roles for item in sublist] #flattening list
all_roles = [item for sublist in all_roles for item in sublist]
for i, v in enumerate(all_roles):
	if '?' in v:
		all_roles[i] = v.translate(None,"?")
	if '_' in v:
		v = v.split('_')
		all_roles[i] = v[0]
all_roles = list(set(all_roles)) #making this a list of unique verbs (removing duplicates)
all_roles = list(filter(None, all_roles)) #removing empty strings

#create list of all frames
all_frames = []
for x in classes_dict:
	frame = gen_dict_extract('frames', x)
	frame = list(frame)
	iterframe = iter(frame)
	next(iterframe)
	for f in iterframe:
		all_frames.append(f['frame'])
all_frames = list(set(all_frames)) #making this a list of unique verbs (removing duplicates)
all_frames = list(filter(None, all_frames)) #removing empty strings

def first_choice(search_term):
	'''Based on search term selected, returns list for second choice for shiny'''
	if search_term == 'verb':
		return(all_verbs)
	elif search_term == 'class':
		return(class_list)
	elif search_term == 'role':
		return(all_roles)
	elif search_term == 'frame':
		return(all_frames)




