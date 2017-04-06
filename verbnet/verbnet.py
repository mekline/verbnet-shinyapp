import shlex
import itertools
import os
import json
import glob
import cPickle as pickle

def x_strip(x,split):
	'''stripping formatting for xml files'''
	x = x.split( )
	x = x[1]
	x = x.split(split)
	x = shlex.split(x[1])
	x = x[0] #string
	return(x)

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
		elif '<MEMBERS>' in x:
			members_values = []
		elif 'MEMBER name=' in x:
			x=x.split("\"")		
			name = x[1]
			if len(x)<6:
				x.extend(['', '', ''])
			if x[5] != '':
				name = x[5] #if there are more than one version of a verb, then use the version with additional numbers attached
			members_values.append(name)
		elif '<MEMBERS/>' in x:
			members_dict = {'members':''}
			class_values.append(members_dict)
		elif '</MEMBERS>' in x:
			members_dict = {'members' : members_values}
			class_values.append(members_dict)
		elif '<THEMROLES>' in x:
			roles_key = []
			roles_value = []
		elif '<THEMROLE type' in x:
			role = x_strip(x,'type=')
			roles_key.append(role)
		elif '<SELRESTRS logic=' in x:
		 	x = x.split("\"")
		 	logic = x[1]
		 	roles_value.append(logic)
		elif '</THEMROLES>' in x:
			role_dict = dict(itertools.izip(roles_key,roles_value))
			themrole_dict = {'ThemRole' : role_dict}
			class_values.append(themrole_dict)
		elif '<FRAMES>' in x:
			frame_keys = []
			frame_values = []
		elif '<FRAME>' in x:
			temp_frame_values=[]
			temp_frame_keys=[]
		elif 'DESCRIPTION' in x:
			x = x.split("\"")
			temp_frame_keys.append('frame')
			temp_frame_values.append(x[3])
		elif '<SYNTAX>' in x:
			syntax_keys = []
			syntax_values = []
		elif '<NP value=' in x:
			syntax_keys.append('NP')
			x = x_strip(x,'value=')
			syntax_values.append(x)
		elif '<VERB value=' in x:
			syntax_keys.append('VERB')
			x = x_strip(x,'value=')
			syntax_values.append(x)
		elif '<ADV value=' in x:
			syntax_keys.append('ADV')
			x = x_strip(x,'value=')
			syntax_values.append(x)
		elif '<PREP value=' in x:
			syntax_keys.append('PREP')
			x = x.split( )
			x = x[1]
			x = x.split('value=')
			x = x[1]
			x = x.replace('>', '')
			syntax_values.append(x)
		elif '</SYNTAX>' in x:
			syntax_d = dict(itertools.izip(syntax_keys,syntax_values))
			temp_frame_keys.append('syntax')
			temp_frame_values.append(syntax_d)
		elif '<SEMANTICS>' in x:
			semantics_keys = []
			semantics_values = []
		elif '<PRED value' in x:
			semantics_keys.append('value')
			sem = x_strip(x,'value=')
			semantics_values.append(sem)
		elif '<ARGS>' in x:
			arg_keys = []
			arg_values = []
		elif '<ARG type=' in x:
			arg = x_strip(x,'type=')
			arg_keys.append(arg)
			x = x.split( )
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
		elif '</ARGS>' in x:
			arguments_d = dict(itertools.izip(arg_keys,arg_values))
			temp_frame_keys.append('arguments')
			temp_frame_values.append(arguments_d	)
		elif '</SEMANTICS>' in x:
			semantics_d = dict(itertools.izip(semantics_keys,semantics_values))
			temp_frame_keys.append('semantics')
			temp_frame_values.append(semantics_d)
		elif '</FRAME>' in x:
			tempFrame_d = dict(itertools.izip(temp_frame_keys,temp_frame_values))
			temp_frame_d = {'frames':tempFrame_d}
			frame_values.append(temp_frame_d)
		elif '</FRAMES>' in x:
			frames_dict = {'frames':frame_values}
			class_values.append(frames_dict)
			class_d = {class_keys : class_values}
			classes_dict.append(class_d)
		elif '<VNSUBCLASS ID=' in x: #if there are subclasses, enter them as new dictionaries, clearning the the class values
			class_values = []
			x = x.split('ID=')
			x = shlex.split(x[1])
			x = x[0]
			x = x.replace('>', '')
			class_keys = x

#creating a list of all the xml verbnet files:
file_list = []
for file in os.listdir("/Users/laurenskorb/Repos/shiny_verbnet/verbnet"): #this depends on machine
     if file.endswith(".xml"):
         file_list.append(file)

#creating list of dictionaries of all verb classes from file list created above
classes_dict = [] 
for file in file_list:
 	verbnet_forloop(file)

pickle.dump(classes_dict,open('save.p','wb'))


