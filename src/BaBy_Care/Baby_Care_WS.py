'''
Created on Feb 19, 2014

@author: nabillo
'''

from BaBy_Care import app, log,db, Celery
from Baby_Care_Activity import agitation_ctr_exe, activity_ctr_exe, normal_levels
from flask import request, jsonify

@app.route('/activity_ctr.json', methods=['POST'])
def activity_ctr() :
	"""Control activity.
	
	@Imput    command : [Start,Stop,Event,Calibrate].
			agi_normal (decimal).
	@Return   result : [In progress,Success,Stoped,Error,None].
	"""
	
	log.info('activity_ctr BEGIN')
	
	# Get the JSON data sent from the form
	data = request.get_json(force=True)
	
	log.info(data['command'])
	if (data['command'] == 'Start') :
		result = activity_ctr_start()
	elif (data['command'] == 'Stop') :
		result = activity_ctr_stop()
	elif (data['command'] == 'Event') :
		if (data['state'] == 'Begin') :
			
		elif (data['state'] == 'End') :
			
	elif (data['command'] == 'Calibrate') :
		# Calibrate the normale sound level
		result = normal_levels(data['agi_normal'])
		#TODO : adjust intervals
	else :
		log.warning('invalid command')
		result = 'None'
	
	log.debug(result)
	log.info('activity_ctr END')
	return jsonify(result=result)
	
@app.route('/media_ctr.json', methods=['POST'])
def media_ctr() :
	"""Control media center.
	
	@Imput    command : [Upload,Delete,List,Play,Stop,VolUp,VolDown].
	          titles.
	@Return   result : [%d,list,Success,Error].
	"""
	
	log.info('media_ctr BEGIN')
	
	# Get the JSON data sent from the form
	data = request.get_json(force=True)
	
	log.info(data['command'])
	if (data['command'] == 'Upload') :
		result = media_upload(request.files.getlist("file[]"))
	elif (data['command'] == 'Delete') :
		result = media_del(data['titles'])
	elif (data['command'] == 'List') :
		result = media_list()
	elif (data['command'] == 'Play') :
		result = media_Play()
	elif (data['command'] == 'Stop') :
		result = media_Stop()
	elif (data['command'] == 'VolUp') :
		result = media_VolUp()
	elif (data['command'] == 'VolDown') :
		result = media_VolDown()
	else :
		log.warning('invalid command')
		result = 'None'
	
	log.debug(result)
	log.info('media_ctr END')
	return jsonify(result=result)
	
	
