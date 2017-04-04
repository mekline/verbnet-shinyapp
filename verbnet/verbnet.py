import shlex
import itertools
import os
import json
import glob
import cPickle as pickle

def verbnet_forloop(file):
	"""This function goes through the lines in the verbnet xml file 
	and creates lists of keys and values to make a nested dictionary"""
	POS = open(file,'r')
	POS_list = POS.readlines()
	for x in POS_list:
		if '<VNCLASS ID=' in x:
			class_values = []
			x = x.split('ID=')
			x = shlex.split(x[1])
			class_keys = x[0] #this will always be the main verb class
		if '<MEMBERS>' in x:
			members_values = []
		if 'MEMBER name=' in x:
			x=x.split("\"")		
			name = x[1]
			if len(x)<6:
				x.extend(['', '', ''])
			if x[5] != '':
				name = x[5] #if there are more than one version of a verb, then use the version with additional numbers attached
			members_values.append(name)
		if '<MEMBERS/>' in x:
			members_dict = {'members':''}
			class_values.append(members_dict)
		if '</MEMBERS>' in x:
			members_dict = {'members' : members_values}
			class_values.append(members_dict)
		if '<THEMROLES>' in x:
			roles_key = []
			roles_value = []
		if '<THEMROLE type' in x:
			x = x.split( )
			role = x[1]
			role = role.split('type=')
			role = shlex.split(role[1])
			role = role[0]
			role = role.replace('>', '')
			roles_key.append(role)
		if '<SELRESTRS logic=' in x:
		 	x = x.split("\"")
		 	logic = x[1]
		 	roles_value.append(logic)
		if '</THEMROLES>' in x:
			role_dict = dict(itertools.izip(roles_key,roles_value))
			themrole_dict = {'themroles' : role_dict}
			class_values.append(themrole_dict)
		if '<FRAMES>' in x:
			frame_keys = []
			frame_values = []
		if '<FRAME>' in x:
			temp_frame_values=[]
			temp_frame_keys=[]
		if 'DESCRIPTION' in x:
			x = x.split("\"")
			temp_frame_keys.append('frame')
			temp_frame_values.append(x[3])
		if '<SYNTAX>' in x:
			syntax_keys = []
			syntax_values = []
		if '<NP value=' in x:
			syntax_keys.append('NP')
			x = x.split( )
			x = x[1]
			x = x.split('value=')
			x = shlex.split(x[1])
			x = x[0]
			x = x.replace('>', '')
			syntax_values.append(x)
		if '<VERB value=' in x:
			syntax_keys.append('VERB')
			x = x.split( )
			x = x[1]
			x = x.split('value=')
			x = shlex.split(x[1])
			x = x[0]
			x = x.replace('>', '')
			syntax_values.append(x)
		if '<ADV value=' in x:
			syntax_keys.append('ADV')
			x = x.split( )
			x = x[1]
			x = x.split('value=')
			x = shlex.split(x[1])
			x = x[0]
			x = x.replace('>', '')
			syntax_values.append(x)
		if '<PREP value=' in x:
			syntax_keys.append('PREP')
			x = x.split( )
			x = x[1]
			x = x.split('value=')
			x = x[1]
			x = x.replace('>', '')
			syntax_values.append(x)
		if '</SYNTAX>' in x:
			syntax_d = dict(itertools.izip(syntax_keys,syntax_values))
			temp_frame_keys.append('syntax')
			temp_frame_values.append(syntax_d)
		if '<SEMANTICS>' in x:
			semantics_keys = []
			semantics_values = []
		if '<PRED value' in x:
			semantics_keys.append('value')
			x = x.split( )
			sem = x[1]
			sem = sem.split('value=')
			sem = shlex.split(sem[1])
			sem = sem[0]
			sem = sem.replace('>', '')
			semantics_values.append(sem)
		if '<ARGS>' in x:
			arg_keys = []
			arg_values = []
		if '<ARG type=' in x:
			x = x.split( )
			arg = x[1]
			arg = arg.split('type=')
			arg = shlex.split(arg[1])
			arg = arg[0]
			arg_keys.append(arg)
			if len(x) < 3:
				x.append('value=""/>')
			argv = x[2]
			argv = argv.split('value=')
			argv = argv[1]
			if ',' in argv:
				argv = argv.replace(',','"/>')
			argv = argv.split('/>')
			argv = shlex.split(argv[0])
			arg_values.append(argv)
		if '</ARGS>' in x:
			arguments_d = dict(itertools.izip(arg_keys,arg_values))
			temp_frame_keys.append('arguments')
			temp_frame_values.append(arguments_d	)
		if '</SEMANTICS>' in x:
			semantics_d = dict(itertools.izip(semantics_keys,semantics_values))
			temp_frame_keys.append('semantics')
			temp_frame_values.append(semantics_d)
		if '</FRAME>' in x:
			tempFrame_d = dict(itertools.izip(temp_frame_keys,temp_frame_values))
			temp_frame_d = {'frames':tempFrame_d}
			frame_values.append(temp_frame_d)
		if '</FRAMES>' in x:
			frames_dict = {'frames':frame_values}
			class_values.append(frames_dict)
			class_d = {class_keys : class_values}
			classes_dict.append(class_d)
		if '<VNSUBCLASS ID=' in x: #if there are subclasses, enter them as new dictionaries, clearning the the class values
			class_values = []
			x = x.split('ID=')
			x = shlex.split(x[1])
			x = x[0]
			x = x.replace('>', '')
			class_keys = x

#creating a list of all the xml verbnet files:
file_list = []
for file in os.listdir("/Users/laurenskorb/Documents/L3 Lab Admin Docs/verbnet"): #this depends on machine
     if file.endswith(".xml"):
         file_list.append(file)

#creating list of dictionaries of all verb classes from file list created above
classes_dict = [] 
for file in file_list:
 	verbnet_forloop(file)

pickle.dump(classes_dict,open('save.p','wb'))

#export to a text file
#with open('verbnet_txt', 'w') as fout:
	#json.dump(classes_dict, fout)

