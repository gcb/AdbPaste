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

import sys,subprocess,itertools
class AdbPaste:
	"Pass a long string as input to an android device/emulator"

	def __init__(self, input_string=""):
		self.addString( input_string )
	
	def addString(self, input_string):
		self.string_data = input_string

	def getKeys(self, fast=False):
		if len(self.string_data) > 0:
			r = "$'" + ''.join(['\\x' + c.encode('hex') for c in self.string_data]) + "'"

		return r

	def sendKeys(self, string, device=False, dryrun=False):
		self.send( string, device, dryrun );

	def send( self, string, device=False, dryrun=False ):
		"sends a single key to the device/emulator"
		print('sending', string)
		if dryrun: return
		cmd = ['adb']
		if isinstance(device, str):
			cmd += ['-s', device]
		cmd += ['shell', 'input', 'text', string]
		ret = subprocess.call(cmd)
		if ret != 0:
			if isinstance(ret, int):
				sys.exit( ret )
			else:
				sys.exit( 1 )

def readFrom(f):
	res = f.read()
	if notab:
		import re
		res = re.sub('\t', ' ', res)
	return res

def displayHelp():
	print """
Command: python AdbPaste.py [options [optionArguments]] [text]

Options:

--help,-h: Show this help

--fast: Ignores the workaround of breaking up the longer strings into small batches. Works fine for simple inputs. Will fail if used on emulator with fields that do network lookup.

--notab: Changes tabs into single spaces

-s: Serial number of the device adb should use. Analogous to -s flag of adb (use adb devices to see a list). Only needed if more than one device are available.

-n: Dry run. Echo what the command would do, without actually sending anything via adb.

--file: Next argument must be a filename. Content will be sent.

If --file is not used, and no text argument is specified, text is read from stdin.
"""

if __name__=="__main__":

	device = False
	fast = False
	notab = False

	arg_fast = "--fast"
	arg_notab = "--notab"
	arg_s = "-s"
	arg_dryrun = "-n"
	arg_file = "--file"
	arg_help = "--help"
	arg_help_short = "-h"
	invalidArgMsg = "Invalid %s parameter. Run AdbPaste without any arguments to see help menu."

	arg = sys.argv[1:]

	#// --help,-h : Show help.
	if arg_help in arg or arg_help_short in arg:
		displayHelp()
		sys.exit(1)

	#// --fast: Will bypass the workaround of breaking longer strings
	#//         will mess up input in the browser or other input boxes that does network searchs
	#//         while you are typing. For sure!
	if arg_fast in arg:
		index = arg.index(arg_fast)
		arg.pop(index)
		fast = True

	#// -n : Dry-run. Will not call adb, just echo out what it is doing.
	if arg_dryrun in arg:
		index = arg.index(arg_dryrun)
		arg.pop(index)
		dryrun = True
	else:
		dryrun = False
	
	#// --notab: Convert tabs into spaces. usefull for 'typing' a file into a textarea or field where tab would change focus
	if arg_notab in arg:
		index = arg.index(arg_notab)
		arg.pop(index)
		notab = True

	#// -s: pass the next value to -s flag on the adb command. For selecting which device to use when there's more than one present
	if arg_s in arg:
		index = arg.index(arg_s)
		arg.pop(index) #Removes -s
		if len(arg) == index:
			print invalidArgMsg % arg_s
		else:
			device = arg[index]
			arg.pop(index) #Removes device

	#// -- file: read the contents from a file, and not from stdin
	if arg_file in arg:
		index = arg.index(arg_file)
		arg.pop(index) #Remove --file
		if len(arg) == index:
                        print invalidArgMsg % arg_file
                elif isinstance(arg[index], str):
			with open(arg[index], 'r') as content_file:
				arg = readFrom(content_file)
		else:
			arg = " ".join(arg)
	else:
		arg = " ".join(arg)
		if not arg:
			arg = readFrom(sys.stdin)
		
	paste = AdbPaste( arg )
	keys = paste.getKeys(fast)
	paste.sendKeys(keys, device, dryrun )
