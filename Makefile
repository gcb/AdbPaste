SHELL = /bin/bash -xe

.PHONY: help
help:
	## test


# laziest functional testing.
# TODO: move this to a script. There ought to be a pattern for testing
#       command line scripts in python...
.PHONY: test
test:
	# expected:
	# ('sending', '01234567')
	# ('sending', '\\;asdf')
	# actual:
	python ./AdbPaste.py  -n '01234567;asdf'
	#
	# TODO: add more tests
	
