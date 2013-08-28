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
		#// note how there's not ":" and others... sigh. can't standardize one solution for it all
	}

	#// charaters that must be sent as keyevent because as string sh will complain.
	#// there is nothing i can do when calling it on windows because adb will just
	#// pass it forward to sh and things break.
	trouble = [' '] # i think space is only needed in adb.exe->sh... when running directly in unix it may not be needed
	inconvenience = [';', ')' ,'(', '"', '\'', '\\', '&' ]

	def __init__(self, input_string=""):
		self.addString( input_string )
	
	def addString(self, input_string):
		self.string_data = input_string


	def getKeys(self, fast=False):
		"thanks to some keys not being available, e.g. colon, we return an array of keycodes (int) or strings."
		r = []
		count = 0
		for c in self.string_data:
			count += 1
			# if char is in trouble list, create a new int element in the output
			if c in self.trouble:
				t = self.translate(c)
				r.append( t )
			# work around a bug in the emulator... if the browser starts to look on google
			#  while this script is 'typing' in the address bar, anything longer than 10 or so
			#  chars will fail on my box... so just make it slow here too... man, i hate the emulator.
			#if len(r) < 10: # or len(r[-1]) > 10:
			elif not fast and count > 7 and isinstance(r[-1], str) and len(r[-1]) > 7:
				r.append( c )
			else:
				#// if the last element is a safe string, continue to add to it
				# before anything, escape if needed
				if c in self.inconvenience:
					c = '\\' + c
				if len(r) > 0 and isinstance(r[-1], str):
					r[-1] += c
				else:
					#// otherwise, start a new safe string batch
					r.append( c )
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
	arg = sys.argv[1:]
	if arg[0] == "--fast":
		fast = True
		arg = arg[1:]
	else:
		fast = False
	paste = AdbPaste( " ".join(arg) )
	keys = paste.getKeys(fast)
	paste.sendKeys(keys)
