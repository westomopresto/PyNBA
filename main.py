import csv
import os
import shutil
from shutil import copytree, ignore_patterns
import errno
from xml.dom import minidom


### Classes ###

class shape:
	borrowed = False
	scan = ''
	path = ''

class texture:
	borrowed = False
	map = ''
	path = ''

class player:
	'''Player class that holds locations and attributes for the player files'''
	objs = [] # Paths to ALL unique blendshape OBJs the player might need
	unique_objs = [] # paths to override objs only
	shared_objs = [] # paths to generic objs we didnt override
	textures = [] # paths to ALL unique .tga files the player might need, excluding psd & 4096
	id = 0000
	firstname = "john"
	lastname = "doe"
	player_id = "0000_doe_john"
	_textures = []
	_shapes = []

	def __init__(self, id, firstname, lastname, player_id):
		self.id = id
		self.firstname = firstname
		self.lastname = lastname
		self.player_id = player_id

	def __str__(self):
		return os.path.join("./Players/",self.player_id)
	
	def write_xml(self):
		root = minidom.Document()

		xml = root.createElement('player')
		root.appendChild(xml)
		xml.setAttribute('id', self.id)
		xml.setAttribute('lastname', self.lastname)
		xml.setAttribute('firstname', self.firstname)
		xml.setAttribute('player_id', self.player_id)
		## shapes cateory
		shapes = root.createElement('shapes')
		xml.appendChild(shapes)
		### shape iterate over our array
		for _shape in self._shapes:
			shape = root.createElement('shape')
			shapes.appendChild(shape)
			shape.setAttribute('borrowed', _shape.borrowed)
			shape.setAttribute('scan', _shape.scan)
			shape.setAttribute('path', _shape.path)

		## textures category	
		textures = root.createElement('textures')
		xml.appendChild(textures)
		### textures iterate over our array
		for _texture in self._textures:
			texture = root.createElement('texture')
			textures.appendChild(texture)
			texture.setAttribute('borrowed', _texture.borrowed)
			texture.setAttribute('map', _texture.map)
			texture.setAttribute('path', _texture.path)

		xml_str = root.toprettyxml(indent = "\t")
		path = self.__str__()+"/"
		save_path_file = os.path.join(path, "player.sidecar")
		with open(save_path_file, "w") as f:
			f.write(xml_str)
		return path
	

### FUNCTIONS WE NEED ###

def create_folder(dir, folder): # function to make a folder with a parent folder in mind
	path = os.path.join(dir, folder)
	if not(os.path.exists(path) and os.path.isdir(path)): #checks if the directory exists first
		os.mkdir(path)
	return path

def create_dir(path): # creates a directory at a path location
	if not(os.path.exists(path) and os.path.isdir(path)): #checks if the directory exists first
		os.makedirs(path)
	return path

def prepare_paths(src_path, dst_path): # clean path names
	src_path = os.path.abspath(src_path).replace(os.sep, '/') # cleans the relative path to absolute path
	dst_path = os.path.abspath(dst_path).replace(os.sep, '/')

def copy_file(src_path, dst_path): # Copy file function
	try:
		shutil.copy(src_path,dst_path)
	except shutil.SameFileError:
		print("Source & Destination are the same file")
	except PermissionError:
		print(dst_path)
		print("No proper permissions")
	except FileExistsError:
		print(dst_path)
		print("File Already exists")
	except:
		print(src_path)
		print(dst_path)
		print("An unexpected error occured")

def copy_folder(src_path, dst_path, exclude): # Copy folder
	for filename in os.listdir(src_path):
		s = os.path.join(src_path, filename)
		d = os.path.join(dst_path, filename)
		foundExclusion = False
		for nm in exclude:
			if nm == filename:
				foundExclusion = True
		if foundExclusion:
			print("Found exlusion: "+filename)
		else:
			shutil.copyfile(s,d)


### OUR SPECIFIC NBA NEW PLAYER INITIAL FILES ###

playerDirectory = "./Players/"
newPlayers = os.path.join(playerDirectory,'new_players.csv')

genericMaleBlendShape = '0000_generic_male/_facebuild/blendShapes_scans/c_face_neutral.obj' ## We need this specific file ##

foldersToCopy = [] ## list of folders & their contents to copy ##
foldersToCopy.append("0000_generic_male/_facebuild/models")
foldersToCopy.append("0000_generic_male/_facebuild/rigging")
foldersToCopy.append("0000_generic_male/_facebuild/workingDir")
foldersToCopy.append("0000_generic_male/textures")

exclude = [] ## List of stuff to exclude if we find them ##
exclude.append("0000_face_wrinkleNormal.tga")
exclude.append("0000_face_wrinkleColor.tga")


### OUR SPECIFIC NBA PLAYER SCRIPTING ###

def initalize_folder_structure(id, lastname, firstname, _player):
	userFolderName = id+lastname+firstname
	topFolder = create_folder(playerDirectory, ""+userFolderName) #make the top folder "0420_mitchell_weston" for example, returns path
	src_path = os.path.join(playerDirectory,genericMaleBlendShape)
	dst_path = os.path.join(topFolder+'/'+'_facebuild/blendShapes_scans/')

	prepare_paths(src_path,dst_path) # cleans our directory path names for the Operating system
	create_dir(dst_path) # creates the directory so we dont error out
	copy_file(src_path, dst_path) # Copies the file

	for src in foldersToCopy:
		tarPath = src.replace("0000_generic_male", userFolderName)
		tarPath = os.path.join(playerDirectory, tarPath) ## puts our .player directory relative path in
		src = os.path.join(playerDirectory, src) ## puts our .player directory relative path in
		prepare_paths(src, tarPath)
		create_dir(tarPath)
		##copy_folder(src, tarPath, exclude)
		try:
			shutil.copytree(src, tarPath, dirs_exist_ok=True, ignore=ignore_patterns(*exclude)) ## Converts our array of ignored files to a string pattern to be ignored via shutil,copytree
		except OSError as err:
			if err.errno == errno.ENOTDIR:
				shutil.copy2(src, tarPath)
			else:
				print("Error: % s" % err)

	print(_player.write_xml())

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
				if(firstname == "weston"): ## for testing
					_player = player(id, firstname, lastname, id+lastname+firstname) ## initializes our player object
					initalize_folder_structure(id,lastname,firstname, _player) #copies the stuff over we need
	
initialize_players()



