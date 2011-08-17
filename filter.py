#!/usr/bin/env python

# Remember to sudo apt-get install python-vobject

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
	print
	print outcal.serialize()


def print_form():
	print """Content-Type: text/html;encoding=utf-8

<!DOCTYPE html>
<html><head>
<title>Facebook events filter</title>
<style type="text/css">
input {
	border: 1px solid black;
	background: #EEF;
}

.tip {
	font-family: "Helvetica", "Arial", sans-serif;
	font-size: 70%;
	border: 1px solid #777;
	background-color: #FFC;
	padding: 4px;
	margin-top: 1px;
	width: 25em;
	color: #555;
}
</style>
</head><body>
<h1>Facebook events filter</h1>

<form method="GET">
<label for="src">Your Facebook event feed URI:</label><br/>
<input name="src" type="text" size="90" placeholder="webcal://www.facebook.com/ical/u.php?uid=...&key=..."></input><br/>

<div class="tip">You can find your Facebook event feed URI by clicking the "Export"-link on <a href="https://www.facebook.com/events/">your events page</a></div>

<p>Include only events with the following RSVP statuses:<br/>
<input name="accept" type="checkbox" value="ACCEPTED" checked></input>Attending<br/>
<input name="accept" type="checkbox" value="TENTATIVE" checked></input>Maybe attending<br/>
<input name="accept" type="checkbox" value="DECLINED"></input>Not attending<br/>
<input name="accept" type="checkbox" value="NEEDS-ACTION" checked></input>Waiting for reply<br/>
</p>
<input type="submit" value="Get filtered feed"></input>
</form>
</body></html>
"""


def main(argv):
	form = cgi.FieldStorage()

	if 'src' in form:
		execute_filter(form['src'].value, form.getlist('accept'))
	else:
		print_form()

	return 0


if __name__=='__main__':
	import sys
	sys.exit(main(sys.argv))
