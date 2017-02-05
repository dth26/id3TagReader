
import main
import os
from main import ExtractMetadata

class test:

	def __init__(self):
		path = '/Users/danielhui/Desktop/ipod songs/test'
		list_of_files = []
		self.traverseDirectory(path, list_of_files)

		for path_of_track in list_of_files:
			print path_of_track
			ExtractMetadata(path_of_track)
			print '-------'


		# for fi in list_of_files:


	#
	#	ACTION : traverse a directory and return all paths relative to root
	#	ARGUMENTS :
	#		path => path of dir
	#		list_of_files = this function appends the filename paths found recursively in path 
	#	RETURNS : list of filesname paths relative to root of argument path
	# 
	def traverseDirectory(self, path, list_of_files):
		
		for root, dirs, files in os.walk(path, topdown=True):

			for fn in files:
				file_path = os.path.join(root, fn)
				#print("Found file: " + file_path)
				list_of_files.append(file_path)
				#print fn


			for d in dirs:		# search subdirectory
				sub_path = os.path.join(root,d)
				print('Searching directory :' + sub_path)
				self.traverseDirectory(sub_path, list_of_files)

test()