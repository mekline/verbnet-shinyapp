import cPickle as pickle
import cgi
import json

classes_dict = pickle.load(open('save.p','rb'))

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


def all_verbs(classes_dict=classes_dict):
	'''returns list of all verbs'''
	all_verbs = []
	for x in classes_dict:
		for keys in x:
			if '-' in keys:
				class_verb = keys
		verbs = gen_dict_extract('members',x)
		verbs=list(verbs)
		verbs = [item for sublist in verbs for item in sublist]
		for i, s in enumerate(verbs):
			s = ''.join((s, ' (class: ',str(class_verb),')'))
			verbs[i] = s
		all_verbs.append(verbs)
	all_verbs = [item for sublist in all_verbs for item in sublist]
	all_verbs = set(all_verbs) #making this a list of unique verbs (removing duplicates)
	all_verbs = list(filter(None, all_verbs)) #removing empty strings
	all_verbs = sorted(all_verbs, key=lambda s: s.lower())
	all_verbs.append('')
	return(all_verbs)

def return_verb_list(search_term,search_category):
	'''given search term (class,frame,role), returns list of verbs'''
	if search_category == 'verb':
		return(all_verbs(classes_dict))
	else:
		verbs = []
		for x in classes_dict:
			for keys in x:
				if '-' in keys:
					class_verb = keys
			if search_category == 'frame':
				y = gen_dict_extract('frames', x)
				y = list(y)
				y = [item for sublist in y for item in sublist]
			elif search_category == 'role':
				roles = gen_dict_extract('ThemRole', x)
				roles = list(roles)
				for i, v in enumerate(roles):
					if type(v) == dict:
						roles[i] = v.keys()
				y = [item for sublist in roles for item in sublist]
			elif search_category == 'class':
				my_list = [(k, v) for (k, v) in x.iteritems()]
				y = k
			if search_term in y:
				verb_list = gen_dict_extract('members',x)
				verb_list=list(verb_list)
				verb_list = [item for sublist in verb_list for item in sublist]
				for i, s in enumerate(verb_list):
					s = ''.join((s, ' (class: ',str(class_verb),')'))
					verb_list[i] = s
				verbs.append(verb_list)
		verbs = [item for sublist in verbs for item in sublist]
		verbs = set(verbs)
		verbs = list(filter(None, verbs))
		verbs = sorted(verbs, key=lambda s: s.lower())
		verbs.append('')
		return(verbs)


def class_given_verb(search_verb):
	'''returns the class dictionary that a verb is in'''
	search_verb = search_verb.split('(class: ')
	search_class = search_verb[-1]
	search_class = search_class.replace(')','')
	for x in classes_dict:
		for keys in x:
			if search_class in keys:
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
	correct_class = class_given_verb(search_verb)
	frame = gen_dict_extract('frames', correct_class)
	frame = list(frame)
	frame = [item for sublist in frame for item in sublist] #flattening list
	return(frame)


def roles_given_verb(search_verb,d_list=classes_dict):
	'''given a verb, prints frames for that verb'''
	role_list = []
	correct_class = class_given_verb(search_verb)
	role = gen_dict_extract('ThemRole', correct_class)
	role = list(role)
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

def first_choice(search_term):
	'''Based on search term selected, returns list for second choice for shiny'''
	if search_term == 'verb':
		return('NA')
	elif search_term == 'class':
		class_list = []
		for x in classes_dict:
			my_list = [(k, v) for (k, v) in x.iteritems()]
			verb_class = my_list[0][0]
			class_list.append(verb_class)
		class_list = sorted(class_list, key=lambda s: s.lower())
		class_list.append('')
		return(class_list)
	elif search_term == 'role':
		all_roles = []
		all_roles = []
		for x in classes_dict:
			x = gen_dict_extract('ThemRole', x)
			x = list(x)
			x = [item for sublist in x for item in sublist] #flattening list
			all_roles.append(x)
		all_roles = [item for sublist in all_roles for item in sublist] #flattening list
		all_roles = list(set(all_roles)) #making this a list of unique verbs (removing duplicates)
		all_roles = list(filter(None, all_roles))
		for i, v in enumerate(all_roles):
			if '_' in v:
				v = v.split('_')
				all_roles[i] = v[0]
		for i, v in enumerate(all_roles): 
			if '?' in v:
				all_roles[i] = v.translate(None,'?')
		all_roles = sorted(all_roles, key=lambda s: s.lower())
		all_roles.append('')
		return(all_roles)
	elif search_term == 'frame':
		all_frames = []
		for x in classes_dict:
			frame = gen_dict_extract('frames', x)
			frame = list(frame)
			all_frames.append(frame)
		all_frames = [item for sublist in all_frames for item in sublist]
		all_frames = [item for sublist in all_frames for item in sublist]
		all_frames = list(set(all_frames)) #making this a list of unique frames (removing duplicates)
		all_frames = list(filter(None, all_frames)) #removing empty strings
		all_frames = sorted(all_frames, key=lambda s: s.lower())
		all_frames.append('')
		return(all_frames)


def second_choice(search_term,search2):
	'''after making second choice, gives list of verbs'''
	if search_term == '':
		return('')
	else:
		l = return_verb_list(search2,search_term)
		return(l)

def final_print(verb):
	'''Given final verb, prints all information needed'''
	if verb=='':
		return('')
	frames = frames_given_verb(verb)
	role = roles_given_verb(verb)
	v_class = class_name_given_verb(verb)
	url = "http://verbs.colorado.edu/verb-index/vn/%s.php" % v_class
	return(str(verb) + '\n' +
		'Class: ' + str(v_class) + '\n' +
		'Roles: ' + str(role) + '\n' +
		'Frames: ' + str(frames) + '\n' +
		'Unified Verb Index: ' + str(url))

