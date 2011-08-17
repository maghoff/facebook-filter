#!/usr/bin/env python

# Remember to sudo apt-get install python-vobject

import vobject, urllib2, cgi



def execute_filter(src_uri, acceptable):
	calendar = None

	src = urllib2.urlopen(src_uri)

	# There should be one calendar:
	incal = vobject.readOne(src)
	src.close()

	outcal = vobject.iCalendar()

	for event in incal.components():
		# This is apparently needed for many iCal clients:
		for c in event.contents['class']:
			c.value = 'PUBLIC'

		# This is the filtering part
		rsvp = event.partstat.value
		if rsvp in ACCEPTABLE_PARTSTATUSES:
			#outcal.contents['vcard'].append(event)
			outcal.add(event)

	print "Content-Type: text/calendar;encoding=utf-8"
	print
	print outcal.serialize().decode('utf-8')


def print_form():
	print """<!DOCTYPE html>
<html><head>
<title>Facebook events filter</title>
</head><body>
<form method="GET">
<input name="src" type="text"></input>
<input type="submit"></input>
</form>
</body></html>
"""


def main(argv):
	form = cgi.FieldStorage()

	if 'src' in form:
		execute_filter(form['src'].value, ['ACCEPTED'])
	else:
		print_form()

	return 0


if __name__=='__main__':
	import sys
	sys.exit(main(sys.argv))
