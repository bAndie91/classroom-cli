#!/usr/bin/env python3

import json

from utils import color, gclassroom, logger

def indent(t, level=1, i='\t'):
	import re
	return re.sub(r'^', i*level, t, 0, re.MULTILINE)

def firstOrNone(iterable):
	try:
		first = iterable[0]
	except IndexError:
		first = None
	return first

Classroom = gclassroom.Classroom()
Classroom.initialize()

curses_object = Classroom.service.courses()
curses = curses_object.list(pageSize=100).execute().get('courses')

for curse in curses:
	announcements = curses_object.announcements().list(courseId=curse['id']).execute().get('announcements')
	teachers = curses_object.teachers().list(courseId=curse['id']).execute().get('teachers')
	
	for announ in reversed(announcements):
		creator_teacher = firstOrNone([teacher['profile']['name']['fullName'] for teacher in teachers if teacher['userId'] == announ['creatorUserId']])
		if creator_teacher is not None:
			print(f"From: {creator_teacher}")
		print(f"Curse: {curse['name']}")
		print(f"Date-Created: {announ['creationTime']}")
		if announ['updateTime'] != announ['creationTime']:
			print(f"Date-Updated: {announ['updateTime']}")
		
		for material in announ.get('materials', []):
			if 'driveFile' in material and 'driveFile' in material['driveFile']:
				driveFile = material['driveFile']['driveFile']
				print(f"Attachment: {driveFile['title']} <{driveFile['alternateLink']}>")
			else:
				print(f"Attachment-JSON: {json.dumps(material)}")
		print()
		text = announ['text']
		print(indent(text))
		print()
