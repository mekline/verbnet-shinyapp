import cPickle as pickle
import cgi
import json

classes_dict = pickle.load(open('save.p','rb'))

def class_to_verbs(search):
	'''given the verb class, this function prints all the members in the main verb class and associated subclasses'''
	for x in classes_dict:
		for keys in x:
			if '-' in keys:
				class_verb = keys
		my_list = [(k, v) for (k, v) in x.iteritems()]
		if search in k:
			my_list = my_list[0]
			verb_list = (my_list[1][0]['members'])
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
			return(verb_list)

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

def class_given_verb(search_verb):
	'''returns the class dictionary that a verb is in'''
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
	return(correct_class)

def class_name_given_verb(search_verb):
	'''returns class name given verb'''
	x = class_given_verb(search_verb)
	x = x.keys()
	x = x[0]
	return(x)

def frames_given_verb(search_verb,d_list=classes_dict):
	'''given a verb, prints frames for that verb'''
	frame_list = []
	correct_class = class_given_verb(search_verb)
	frame = gen_dict_extract('frames', correct_class)
	frame = list(frame)
	iterframe = iter(frame)
	next(iterframe)
	for f in iterframe:
		frame_list.append(f['frame'])
	frame_list=list(set(frame_list))
	return(frame_list)

def roles_given_verb(search_verb,d_list=classes_dict):
	'''given a verb, prints frames for that verb'''
	role_list = []
	correct_class = class_given_verb(search_verb)
	role = gen_dict_extract('ThemRole', correct_class)
	role = list(role)
	for i, v in enumerate(role):
		if type(v) == dict:
			role[i] = v.keys()
	role_list.append(role)
	role_list = [item for sublist in role_list for item in sublist] #flattening list
	role_list = [item for sublist in role_list for item in sublist]
	for i, v in enumerate(role_list):
		if '?' in v:
			role_list[i] = v.translate(None,"?")
		if '_' in v:
			v = v.split('_')
			role_list[i] = v[0]
	role_list = list(set(role_list)) #making this a list of unique verbs (removing duplicates)
	role_list = list(filter(None, role_list)) #removing empty strings
	return(role_list)

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
		return('NA')
	elif search_term == 'class':
		return(class_list)
	elif search_term == 'role':
		return(all_roles)
	elif search_term == 'frame':
		return(all_frames)

def frames_to_verbs(search):
	'''given a syntactic frame, gives list of verbs'''
	verbs = []
	for x in classes_dict:
		for keys in x:
			if '-' in keys:
				class_verb = keys
		frame_list = []
		frame = gen_dict_extract('frames', x)
		frame = list(frame)
		iterframe = iter(frame)
		next(iterframe)
		for f in iterframe:
			frame_list.append(f['frame'])
		if search in frame_list:
			my_list = [(k, v) for (k, v) in x.iteritems()]
			my_list = my_list[0]
			verb_list = (my_list[1][0]['members'])
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
			verbs.append(verb_list)
	verbs = [item for sublist in verbs for item in sublist]
	return(verbs)

def roles_to_verbs(search):
	'''given a thematic role, returns list of verbs'''
	verbs = []
	for x in classes_dict:
		for keys in x:
			if '-' in keys:
				class_verb = keys
		roles = gen_dict_extract('ThemRole', x)
		roles = list(roles)
		for i, v in enumerate(roles):
			if type(v) == dict:
				roles[i] = v.keys()
		roles = [item for sublist in roles for item in sublist]
		if search in roles:
			my_list = [(k, v) for (k, v) in x.iteritems()]
			my_list = my_list[0]
			verb_list = (my_list[1][0]['members'])
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
			verbs.append(verb_list)
	verbs = [item for sublist in verbs for item in sublist]
	return(verbs)

def second_choice(search_term,search2):
	'''after making second choice, gives list of verbs'''
	if search_term == 'verb':
		return(all_verbs)
	elif search_term == 'class':
		l = class_to_verbs(search2)
	elif search_term == 'role':
		l = roles_to_verbs(search2)	
	elif search_term == 'frame':
		l = frames_to_verbs(search2)
	return(l)

def final_print(verb):
	'''Given final verb, prints all information needed'''
	frames = frames_given_verb(verb)
	role = roles_given_verb(verb)
	v_class = class_name_given_verb(verb)
	return(str(verb) + '\n' +
		'Class: ' + str(v_class) + '\n' +
		'Roles: ' + str(role) + '\n' +
		'Frames: ' + str(frames))

test=roles_given_verb('accept')
print(test)