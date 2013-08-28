#!/usr/bin/python


import sys,os

class AdbPaste:
	"Pass a long string as input to an android device/emulator"

	key_dict = {
		#key is the string, value is the keycode the emulator expects to generate that string
		"0":7,
		"1":8,
		"2":9,
		"3":10,
		"4":11,
		"5":12,
		"6":13,
		"7":14,
		"8":15,
		"9":16,
		"*":17,
		"#":18,
		"A":29,
		"B":30,
		"C":31,
		"D":32,
		"E":33,
		"F":34,
		"G":35,
		"H":36,
		"I":37,
		"J":38,
		"K":39,
		"L":40,
		"M":41,
		"N":42,
		"O":43,
		"P":44,
		"Q":45,
		"R":46,
		"S":47,
		"T":48,
		"U":49,
		"V":50,
		"W":51,
		"X":52,
		"Y":53,
		"Z":54,
		",":55,
		".":56,
		"	":61,
		" ":62,
		"\n":66,
		"`":68,
		"-":69,
		"=":70,
		"[":71,
		"]":72,
		"\\":73,
		";":74,
		"'":75,
		"/":76,
		"@":77,
		"+":81,
		"(":162,
		")":163,
	}

	def __init__(self, input_string=""):
		self.addString( input_string )
	
	def addString(self, input_string):
		self.string_data = input_string


	def getKeys(self):
		"thanks to some keys not being available, e.g. colon, we return an array of keycodes (int) or strings."
		r = []
		for c in self.string_data:
			try:
				t = self.translate(c)
			except KeyError:
				t = c
			r.append( t )
		return r

	def sendKeys(self, key_list):
		for k in key_list:
			self.send( k );

	def send( self, key ):
		"sends a single key to the device/emulator"
		print('sending', key)
		if( isinstance(key, int) ):
			os.system('adb shell input keyevent %d'%key)
		else:
			if( key == '"' ):
				raise Exception(NotImplemented)
			os.system('adb shell input text "' + key + '"')

	def translate( self, char ):
		return self.key_dict[char] #// will fail on unkown values, so we can add them :)





if __name__=="__main__":
	paste = AdbPaste( " ".join(sys.argv[1:]) )
	keys = paste.getKeys()
	paste.sendKeys(keys)
