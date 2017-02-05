class ID3Tag:
	"ID3 Tag"


	def __init__(self):

		self.hdr = {}

		# header
		self.hdr = {
			'file_id' : '',
			'version' : '',
			'flags' : [],
			'size' : 0
		}

		self.title = ''
		self.artist = ''


