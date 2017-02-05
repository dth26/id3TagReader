


class TagAbstract(object):
	""" Interface that ID3V2 ID3V1 class must inherit and override methods """

	def test(self):
		raise NotImplementedError('subclass must override test()')

	def getTitle(self, f):
		raise NotImplementedError('subclass must override getTrackTitle()')

	# def getArist(self):
	# 	raise NotImplementedError('subclass must override getArist()')

	def setTitle(self, f):
		raise NotImplementedError('subclass must override setTitle()')

	# def setArtist(self):
	# 	raise NotImplementedError('subclass must override setArtist()')