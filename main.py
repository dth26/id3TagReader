
from struct import *

from track import ID3Tag
from tagMethods import TagAbstract
import logging


class ExtractMetadata:
	""""Extract metadata from the id3 tag of a file
	
		Attributes :
			title => string,
			artist => string,
			album => string,
			year => 
			comment => string,
	"""


	id3v1_data_mapping= {
		'title'   : (3 , 33),
		'artist'  : (33, 63),
		'album'   : (63, 93),
		'year'    : (93, 97),
		'comment' : (97, 126),
		'genre'	  : (127, 128)
	}

	

	#	Seek, Read file.
	#
	#	Params
	#		path: 		type => string
	#			  	 	desc => full filepath to song
	#		correct: 	type => boolean
	#			     	desc => resolve capitalization errors, and trimming if set to True
	def __init__(self, path):
		#path='/Users/danielhui/Desktop/ipod songs/ADLW.mp3'

		f = open(path, 'rb', 0)
		meta_tag = f.read()
		
		
		# check curr file for ID3v2 and ID3v1 support
		hasID3V2Tag = ID3V2Parser.isID3V2(meta_tag)
		hasID3V1Tag = ID3V1Parser.isID3V1(meta_tag) 
		id3_tag = None
		tag_parser = None


		if(hasID3V2Tag):
			id3_tag = ID3V2Parser(meta_tag)
		elif (hasID3V1Tag):
			id3_tag = ID3V1Parser(meta_tag)
		else:
			# use for testing
			parsed_path = path.split('/')

			folder = parsed_path[-2]
			filename = parsed_path[-1]

			error_out = '%s/%s => neither ID3v1 nor ID3v2 tag found ' % (folder, filename)

			logging.info(error_out)
			print error_out





		# title = self.tag_data[3:33]
		# artist = self.tag_data[33:63]
		
		#for opt, (start, end) in self.tag_data_mapping.items():
			#self[opt] = self.tag_data[start:end]
			#print self.tag_data[start:end]
			#print 'fuck'


	def resolve(self):
		pass

	# 	Show all attributes of this file
	def list_attribute(self):
		attributes = dir(ExtractMetadata)
		print attributes


# 2.4.0
class ID3V2Parser(TagAbstract):	 # must implement methods from TagAbstract
	""" 
		ID3 Tag Structure [x] == # of bytes :

			= ID3v2 header [10]
				- file identifier  [3]     "ID3"
     			- version          [2]      $04 00
     			- flags            [1]      %abcd0000
     			- size       	   [4]      4 * %0xxxxxxx

     	Attributes :
     		= meta_tag
     			- array storing bytes of ID3 tag
     		= id3_tag
     			- meta tag object storing track metadata
	"""

	# option : (start,end,format character for struct)
	main_hdr_struct = {
		'file_id' : (0,3,'3s'),
		'version' : (3,5,'h'),
	    'flags' : (5,6,'1c'),
	    'size' : (6,10,'i')
	}


	def __init__(self, meta_tag):
		self.id3_tag = ID3Tag()
		self.meta_tag = meta_tag #

		#print meta_tag[0:3

		for opt, (start, end, format_char) in self.main_hdr_struct.items():
			val = unpack(format_char, self.meta_tag[start:end])
			self.id3_tag.hdr[opt] = val[0]
			#print opt,':', self.id3_tag.hdr[opt]

		print  "ID3v2."+str(self.id3_tag.hdr['version'])

		#print 'Version 3v',self.id3_tag.hdr['file_id']
		self.findFrames()

		# print self.id3_tag.hdr['file_id'] + 'V2.' + self.id3_tag.hdr['version']
		# print '   flags -> ' + self.id3_tag.hdr['flags']
		# print '   size  -> ' + self.id3_tag.hdr['size']
		#print "extended header: " + self.id3_tag.hdr['flags']['ext_hdr']



	##============================================================================================
	#	ID3V2.3 ID3V2.4
	#	
	#		Frame Header
	#			=> Frame ID      $xx xx xx xx  (4 bytes) 
	#			=> Size      4 * %0xxxxxxx	   (4 bytes)
    #			=> Flags         $xx xx		   (2 bytes)	
	#
	#		Frame IDs:	
	#			=> TIT2
	# 				- 	The 'Title/Songname/Content description' frame is the actual name of
	# 					the piece (e.g. "Adagio", "Hurricane Donna").
	#============================================================================================
	#	ID3V2.2
	#
	# 		./test/GIVS.mp3
	#	 	./test/DWAH.mp3
	#
	#		Frame Header
	#			=> Frame ID      $xx xx xx   (3 bytes) 
	#			=> Size      	 $xx xx xx   (3 bytes)
	#
	#
	



	# ID3V2.x
	# decribes frame header info
	# the key x describes the tags major value
	frame_hdr_structs = {
		# ID3V2.2
		2: {	
			'attrs' : {			
				'id': (0,3),						# relative to frame start index, id starts at index 0 and ends at index 3
				'size': (3,6)
			},
			'hdr_size' : 6, 						# frame header size
			'song_frame_size': 30					# TT2 or TIT2	

		},
		3: {				# ID3V2.3
			'attrs' : {	
				'id': (0,4),
				'size': (4,8),
				'flags': (8,10)
			},
			'hdr_size' : 10, 						# frame header size
			'song_frame_size': None					# TT2 or TIT2	
		},
		4: {
			'attrs' : {
				'id': (0,4),
				'size': (4,8),
				'flags': (8,10)
			},
			'hdr_size' : 10,
			'song_frame_size': None					# TT2 or TIT2	
		}
	}


	def findFrames(self):
		# major version of the tag
		# the x value in ID3v2.x
		tag_maj_vers= self.id3_tag.hdr['version']
		frame_hdr_struct = self.frame_hdr_structs[tag_maj_vers]
		frame_attrs = {
			'id': None,
			'size': None,
			'flags': None
		}
		 
		frame_start = 10

		while( frame_start < len(self.meta_tag) ):

			for opt, (start,end) in frame_hdr_struct['attrs'].items():
				#
				#	opt = size|flags|id
				#
				
				frame_attrs[opt] = self.meta_tag[ (frame_start + start):(frame_start + end) ]
				#print opt,start,end, frame_attrs[opt]

				if opt=='size':
					#frame_attrs['size'] = [ord(b) for b in frame_attrs['size'] ]
					frame_size_str = ''.join(str(ord(s)) for s in frame_attrs['size'])
					frame_attrs['size'] = int(frame_size_str)

 			# parse song name
 			# TIT2 => ID3V2.3, ID3V2.4
 			# TT2 => ID3V2.2
			if frame_attrs['id']=='TIT2' or frame_attrs['id']=='TT2':
				song_name_start = (
					frame_start +
					frame_hdr_struct['hdr_size']
				)
				

		
				song_name_end = song_name_start + frame_attrs['size']


				song_name = self.meta_tag[song_name_start:song_name_end]

				#print ,'; size: ',frame_attrs['size']
				print song_name

			
			frame_hdr_size = frame_hdr_struct['hdr_size']
			frame_start += (frame_attrs['size'] + frame_hdr_size)		# (size of frame content + size of frame header)




			
		
	def extractHdrFlags(self):
		flags = []
		flags_data = self.meta_tag.read(1)
		#print 'flags data: ' + flags_data
		return

		flags.unsynchronisation = ( (flags_data&128) != 0)
		flags.ext_hdr = ((flags_data&64) != 0)					# extended header
		flags.exp_indicator = ((flags_data&32) != 0)			# experimental indicator
		flags.footer = ((flags_data&16) != 0) 

		return flags

	# tags with 'ID3' in first 3 bytes of file is an ID3v2 tag
	@staticmethod
	def isID3V2(meta_tag):
		return (meta_tag[0:3] == 'ID3')


	def getTitle(self):
		pass

	def setTitle(self):
		pass




class ID3V1Parser(TagAbstract):		# must implement methods from TagAbstract

	def __init__(self, meta_tag):
		self.meta_tag = meta_tag
		song_name = meta_tag[-125:-95]
		print 'ID3V1'
		print song_name

		

	@staticmethod
	def isID3V1(meta_tag):
		return meta_tag[-128:-125] == 'TAG'

	def getTitle(self):
		pass

	def setTitle(self):
		pass




if __name__=='__main__':
	pass
	#ExtractMetadata()