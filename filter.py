#!/usr/bin/env python

#import cgi; import cgitb; cgitb.enable()

import vobject, urllib2, cgi



def execute_filter(src_uri, acceptable):
	calendar = None

	if src_uri.startswith('webcal:'):
		src_uri = 'http:' + src_uri[7:]

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
		if rsvp in acceptable:
			outcal.add(event)

	print "Content-Type: text/calendar;encoding=utf-8"
	print "Content-Disposition: attachment;filename=myfbfilter.ics"
	print
	print outcal.serialize()

	return 0


def emit_error():
	print "Content-Type: text/plain"
	print ""
	print "Missing src query parameter. Try again"
	return 1


def main(argv):
	form = cgi.FieldStorage()

	if 'src' in form:
		return execute_filter(form['src'].value, form.getlist('accept'))
	else:
		return emit_error()


if __name__=='__main__':
	import sys
	sys.exit(main(sys.argv))
