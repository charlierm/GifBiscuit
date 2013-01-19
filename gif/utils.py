import random
from grapefruit import Color

class Utils(object):
	
	@classmethod
	def random_colour(cls):
		"""
		Retuns a random HTML colour string.
        
		Returns a random hexidecimal colour string for use in ColorFields. 
		"""
		decimal_value = random.randint(0,16777215) #16777215 = (16^6)-1, or #FFFFFF in Hex
		hex_value = hex(decimal_value) #Convert to hex... prefixed with 0x, though.
		return str(hex_value)[2:]
	
	@classmethod
	def get_complementing_colour(cls, colour):
		"""
		Returns a complementing colour to the hex colour.
		
		Returns a complementing colour to the hex colour supplied as a string.
		"""
		compl = Color.NewFromHtml(colour).ComplementaryColor()
		return compl.html
	
	@classmethod
	def get_colour_pair(cls):
		"""
		Returns a complementing colour pair as a tuple.
		"""
		colours = []
		colours.append(cls.random_colour())
		colours.append(cls.get_complementing_colour(colours[0])[1:])
		return tuple(colours)