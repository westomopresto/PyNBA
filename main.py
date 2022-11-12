import csv
import os
import shutil

playerDirectory = "./Players/"
newPlayers = os.path.join(playerDirectory,'new_players.csv')

def create_folder(dir, folder): # function to make a folder with a parent folder in mind
	path = os.path.join(dir, folder)
	if not(os.path.exists(path) and os.path.isdir(path)): #checks if the directory exists first
		os.mkdir(path)
	return path

def create_dir(path):
	if not(os.path.exists(path) and os.path.isdir(path)): #checks if the directory exists first
		os.makedirs(path)
	return path

def initalize_folder_structure(id,lastname,firstname):
	topFolder = create_folder(playerDirectory, ""+id+lastname+firstname) #make the top folder "0420_mitchell_weston" for example, returns path
	src_path = os.path.join(playerDirectory,'0000_generic_male/_facebuild/blendShapes_scans/c_face_neutral.obj')
	dst_path = os.path.join(topFolder+'/'+'_facebuild/blendShapes_scans/')

	src_path = os.path.abspath(src_path).replace(os.sep, '/') # cleans the relative path to absolute path
	dst_path = os.path.abspath(dst_path).replace(os.sep, '/')
	
	create_dir(dst_path) # creates the directory so we dont error out
	
	try:
		shutil.copy(src_path,dst_path)
	except shutil.SameFileError:
		print("Source & Destination are the same file")
	except PermissionError:
		print("No proper permissions")
	except FileExistsError:
		print("File Already exists")
	except:
		print("An unexpected error occured")
		print(src_path)
		print(dst_path)


def initialize_players():
	with open(newPlayers, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			id = row['id']+"_" #bare minimum underscore shoved in here
			lastname = row['lastname']
			firstname = row['firstname']
			
			if(id != "" and firstname != ""): #Checks if the ID & First name are valid, the only two we need to build a directory (at Minimum)
				if(lastname != ""):
					lastname = lastname+"_" #if the last name exists, shove in an extra underscore, otherwise its empty anyways
				if(firstname == "weston"):
					initalize_folder_structure(id,lastname,firstname) #copies the stuff over we need
	
initialize_players()
