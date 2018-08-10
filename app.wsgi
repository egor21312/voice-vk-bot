#!/usr/bin/env python3
import os
from os import path
import sys
import json
import speech_recognition as sr
from pydub import AudioSegment
import vk
print(sys.version)
os.chdir(os.path.dirname(__file__))
import bottle
application = bottle.default_app()
token = '8c87f13e0ae769de7c46b137f3a170011f1cddec45a6ec02a8a5043cdb454fa2064cc56a3479a78c71bb8'
confirmation_token = '5968cccb'
from bottle import route, post, request
@route('/')
def hello():
	return sys.version
@route('/', method='POST')
def processing():
	postdata = request.body.read()
	print(postdata) #this goes to log file only, not to client
	data = json.loads(request.body.read())
	print(data)
	if 'type' not in data.keys():
		return 'not vk'
	if data['type'] == 'confirmation':
		return confirmation_token
	elif data['type'] == 'message_new':
		session = vk.Session()
		api = vk.API(session, v='5.80')
		user_id = data['object']['peer_id']
		print(user_id)
		from_id = str(data['object']['from_id'])
		attachment = data['object'].get('attachments')
		if attachment:
			isdoc = data['object']['attachments'][0].get('doc')
			if isdoc:
				if data['object']['attachments'][0]['doc'].get('preview'):
					if 'audio_msg' in data['object']['attachments'][0]['doc']['preview']:
						os.system('wget ' + data['object']['attachments'][0]['doc']['preview']['audio_msg']['link_mp3'] + ' -O voice.mp3')
						sound = AudioSegment.from_mp3("/var/www/vk_voicy/voice.mp3")
						sound.export("/var/www/vk_voicy/voice.wav", format="wav")
						print(sound)
						os.remove('/var/www/vk_voicy/voice.mp3')
						AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "voice.wav")
						r = sr.Recognizer()
						print(r)
						with sr.AudioFile(AUDIO_FILE) as source:
							audio = r.record(source)  # read the entire audio file
						try:
							ur_msg=r.recognize_google(audio, language='ru_RU')
						except sr.UnknownValueError:
							ur_msg='Простите, бот Вас не понял.'
						print(ur_msg)
						os.remove('/var/www/vk_voicy/voice.wav')
						api.messages.send(access_token=token, peer_id=user_id, message=ur_msg)
						return 'ok'
		else:
			return 'ok'
