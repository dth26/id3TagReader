
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

	main_hdr_struct = {
		'file_id' : (0,3),
		'version' : (3,5),
		'flags' : (5,6),
		'size' : (6,10)
	}


	def __init__(self, meta_tag):
		self.id3_tag = ID3Tag()
		self.meta_tag = meta_tag #

		#print meta_tag[0:3]

		for opt, (start, end) in self.main_hdr_struct.items():
			self.id3_tag.hdr[opt] = self.meta_tag[start:end]

		self.findFrames()

		# print self.id3_tag.hdr['file_id'] + 'V2.' + self.id3_tag.hdr['version']
		# print '   flags -> ' + self.id3_tag.hdr['flags']
		# print '   size  -> ' + self.id3_tag.hdr['size']
		#print "extended header: " + self.id3_tag.hdr['flags']['ext_hdr']



	#
	#	search file metadata for frames
	#	Frame Header
	#		=> Frame ID      $xx xx xx xx  (4 bytes) 
	#		=> Size      4 * %0xxxxxxx	   (4 bytes)
    #		=> Flags         $xx xx		   (2 bytes)
	#	
	#	Frame IDs:	
	#		=> TIT2
	# 			- 	The 'Title/Songname/Content description' frame is the actual name of
	# 				the piece (e.g. "Adagio", "Hurricane Donna").

	#
	#
	#	10:14 TIT2
	#	14:18 \x00\x00\x00\x12
	#	18:20 Flags
	# 	20:20+18 Song name
	def findFrames(self):
		FRAME_START_POS = 10
		frame_start = FRAME_START_POS

		while( frame_start < len(self.meta_tag) ):
			frame_id = self.meta_tag[frame_start:(frame_start+4)]

		
			# frame_size_str = (
			# 		str(ord( self.meta_tag[(ptr+4):(ptr+5)] )) +
			# 		str(ord( self.meta_tag[(ptr+5):(ptr+6)] )) +
			# 		str(ord( self.meta_tag[(ptr+6):(ptr+7)] )) +
			# 		str(ord( self.meta_tag[(ptr+7):(ptr+8)] ))
			# 	)

			frame_size_list = [
				str(ord( self.meta_tag[(frame_start+4):(frame_start+5)] )) ,
				str(ord( self.meta_tag[(frame_start+5):(frame_start+6)] )) ,
				str(ord( self.meta_tag[(frame_start+6):(frame_start+7)] )) ,
				str(ord( self.meta_tag[(frame_start+7):(frame_start+8)] ))
			]


			#frame_size_str_arr = list(frame_size_list) 
			frame_size_str = ''.join(str(s) for s in frame_size_list)
			frame_size = int(frame_size_str)

			flags_in_bytes = 2 			# bytes
			size_in_bytes = 4  		# size in bytes
			frame_id_in_bytes = 4

			#print "frame data: " + self.meta_tag[(ptr+8):(ptr+8+frame_size)]

			# 10:14	TITV
			# 14:18 x00\x00\x00\x12
			# 18:
 
 			# parse song name
			if(frame_id=='TIT2'):
				song_name_start = (
					frame_start +
					frame_id_in_bytes +
					size_in_bytes +
					flags_in_bytes 
				)

				song_name_end = song_name_start + frame_size
				
				song_name = self.meta_tag[song_name_start:song_name_end]


				print 'Frame ID: ' ,frame_id
				print 'Frame Size: ',frame_size
				print song_name

			# format size from 4 hex values to hex string so we can convert to int form
			# frame_size_str = '{1}{2}{3}{4}'.format(
			# 		ord( self.meta_tag[(ptr+4):(ptr+5)] ),
			# 		ord( self.meta_tag[(ptr+5):(ptr+6)] ),
			# 		ord( self.meta_tag[(ptr+6):(ptr+7)] ),
			# 		ord( self.meta_tag[(ptr+7):(ptr+8)] )
			# 	)

			frame_header_size = 10
			frame_start += (frame_size + frame_header_size)



			
		
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
		pass

	@staticmethod
	def isID3V1(meta_tag):
		return (meta_tag[-128:-125] == 'TAG')

	def getTitle(self):
		pass

	def setTitle(self):
		pass




if __name__=='__main__':
	pass
	#ExtractMetadata()