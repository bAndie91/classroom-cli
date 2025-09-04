#!/usr/bin/env python3

import json

from utils import color, gclassroom, logger

def indent(t, i='\t'):
	import re
	return re.sub(r'^', i, t, 0, re.MULTILINE)


Classroom = gclassroom.Classroom()
Classroom.initialize()

curses = Classroom.service.courses().list(pageSize=100).execute().get('courses')

for curse in curses:
	print("{name}".format_map(curse))
	announcements = Classroom.service.courses().announcements().list(courseId=curse['id']).execute().get('announcements')
	for announ in announcements:
		datetime_info = '\t'.join([announ['creationTime'], announ['updateTime'] if announ['updateTime'] != announ['creationTime'] else ''])
		print(indent(datetime_info))
		text = announ['text']
		print(indent(indent(text)))
