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
			y = x.split('ID=')
			y = shlex.split(y[1])
			class_keys = y[0] #this will always be the main verb class
		elif '<MEMBERS>' in x:
			members_values = []
		elif 'MEMBER name=' in x:
			y=x.split("\"")		
			name = y[1]
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
			role = role.replace('>', '')
			roles_key.append(role)
		elif '</THEMROLES>' in x:
			themrole_dict = {'ThemRole' : roles_key}
			class_values.append(themrole_dict)
		elif '<FRAMES>' in x:
			frame_values = []
		elif 'DESCRIPTION' in x:
			x = x.split("\"")
			frame_values.append(x[3])
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


