#!/usr/bin/python

#
#   Copyright 2013 https://github.com/gcb
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import sys,os,itertools
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
		#// note how there are no :'"? and others... sigh. can't standardize one solution for it all
	}

	#// charaters that must be sent as keyevent because as string sh will complain.
	#// there is nothing i can do when calling it on windows because adb will just
	#// pass it forward to sh and things break.
	trouble = [' ', '\n', '	'] # i think space is only needed in adb.exe->sh... when running directly in unix it may not be needed
	if sys.platform != "win32":
		trouble.append('`')
	inconvenience = [';', ')' ,'(', "'", '\\', '&', '#', '<', '>', '|']

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
				if c == '"': # added this to CMD.exe issues, TODO: test on other platforms
					c = '\\\\\\"' # this will become \\\" to CMD when passing to adb.exe, which will become \" to sh, and finally " to the device
				# special case for > ,only way to escape them in windows when it is in a double quote and followed by anything is with ^
				# but adding the ^ in front, if there's no double quote in the string, CMD will not treat ^ as a special char and send it along
				elif sys.platform == "win32" and c == ">":
					if len(r)>0 and isinstance(r[-1], str) and '"' in r[-1]:
						c = "\\^>"
					else:
						c = "\\>"
				# ^ is a escape char in windows. it will be ignored
				elif sys.platform == "win32" and c == "^":
					c = "^^"
				elif c in self.inconvenience:
					c = '\\' + c

				#// here is something weird... $ does not need to be encoded (\$ results in \$ typed in the emulator) but it will
				#// also fail if it's not the last char in the string. proably sh at some point try to do variable subst
				if len(r) > 0 and isinstance(r[-1], str) and r[-1][-1] != '$':
					r[-1] += c
				else:
					#// otherwise, start a new safe string batch
					r.append( c )

		# ? is a special case at least on win32. "asd?" and "?a" ok. "?" fail. "\?" shows "d".
		# so we can't escape it, but we can make it work by appending something when it is alone.
		# but then we have to delete that something... argh
		# also we only need to pad it if the string isn't already paddig it. but in the main loop we aren't looking forward.
		# so the solution here is to look at instances where it happens without any padding, and change to ?a<backspace>... sigh
		r = itertools.chain.from_iterable(("?a", 67) if item == "?" else (item, ) for item in r)

		return r

	def sendKeys(self, key_list, device = False):
		for k in key_list:
			self.send( k, device );

	def send( self, key, device = False ):
		"sends a single key to the device/emulator"
		print('sending', key)
		cmd = 'adb'
		if isinstance(device, str):
			cmd += ' -s ' + device
		if( isinstance(key, int) ):
			ret = os.system(cmd + ' shell input keyevent %d'%key)
		else:
			ret = os.system(cmd + ' shell input text "' + key + '"')
		if ret != 0:
			if isinstance(ret, int):
				sys.exit( ret )
			else:
				sys.exit( 1 )

	def translate( self, char ):
		return self.key_dict[char] #// will fail on unkown values, so we can add them :)

if __name__=="__main__":
	device = False
	arg = sys.argv[1:]
	#// --fast: must be 1st arg, i'm lazy. Will bypass the workaround of breaking longer strings
	#//         will mess up input in the browser or other input boxes that does network searchs
	#//         while you are typing. For sure!
	if arg[0] == "--fast":
		fast = True
		arg = arg[1:]
	else:
		fast = False
	
	#// --notab: Convert tabs into spaces. usefull for 'typing' a file into a textarea or field where tab would change focus
	if arg[0] == "--notab":
		notab = True
		arg = arg[1:]
	else:
		notab = False

	#// -s: pass the next value to -s flag on the adb command. For selecting which device to use when there's more than one present
	if arg[0] == "-s":
		device = arg[1]
		arg = arg[2:]

	#// -- file: read the contents from a file, and not from stdin
	if arg[0] == "--file" and isinstance(arg[1], str):
		with open(arg[1], 'r') as content_file:
			arg = content_file.read()
			import re
			arg = re.sub('\t', ' ', arg)
	else:
		arg = " ".join(arg)
		
	paste = AdbPaste( arg )
	keys = paste.getKeys(fast)
	paste.sendKeys(keys, device )
