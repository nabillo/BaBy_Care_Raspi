'''
Created on Feb 19, 2014

@author: nabillo
'''

from BaBy_Care import app, log,db, Celery
from Baby_Care_Stream import steam_ctr_start, steam_ctr_stop, steam_ctr_restart
from Baby_Care_Activity import agitation_ctr_exe, activity_ctr_exe, normal_levels
from flask import request, jsonify

@app.route('/stream_ctr.json', methods=['POST'])
def stream_ctr() :
	"""Control streamer.
	
	@Imput    command : [Start,Stop,Restart].
	@Return   result : [Success,Error,None].
	"""
	
	log.info('stream_ctr BEGIN')
	
	# Get the JSON data sent from the form
	data = request.get_json(force=True)
	
	log.info(data['command'])
	if (data['command'] == 'Start') :
		result = steam_ctr_start()
	elif (data['command'] == 'Stop') :
		result = steam_ctr_stop()
	elif (data['command'] == 'Restart') :
		result = steam_ctr_restart()
	else :
		log.warning('invalid command')
		result = 'None'
	
	log.debug(result)
	log.info('stream_ctr END')
	return jsonify(result=result)

@app.route('/activity_ctr.json', methods=['POST'])
def activity_ctr() :
	"""Control activity.
	
	@Imput    command : [Start,Stop,Calibrate].
			agi_normal (decimal).
	@Return   result : [In progress,Success,Stoped,Error,None].
	"""
	
	log.info('activity_ctr BEGIN')
	
	# Get the JSON data sent from the form
	data = request.get_json(force=True)
	
	log.info(data['command'])
	if (data['command'] == 'Start') :
		result = 'Error'
		if ((db.has_key('act_job_id')) and (db['act_job_id'] != '')) :
			result = 'In progress'
		else :
			# Start the agitation controller
			agi_job = agitation_ctr_exe.delay()
			result = agi_job.AsyncResult(agi_job.id).state
			if (result == states.SUCCESS) :
				# Start the activity controller
				act_job = activity_ctr_exe.delay()
				result = act_job.AsyncResult(act_job.id).state
				if (result == states.SUCCESS) :
					result = 'Success'
					db['act_job_id'] = act_job.AsyncResult(act_job.id).id
	elif (data['command'] == 'Stop') :
		result = 'Error'
		if ((not db.has_key('act_job_id')) or (db['act_job_id'] == '')) :
			result = 'Stoped'
		else :
			# Stop the activity controller
			revoke(act_job.id, terminate=True, signal='SIGTERM')
			result = act_job.AsyncResult(act_job.id).state
			if (result == states.REVOKED) :
				# Stop the agitation controller
				revoke(agi_job.id, terminate=True, signal='SIGTERM')
				result = agi_job.AsyncResult(agi_job.id).state
				if (result == states.REVOKED) :
					result = 'Success'
					db['act_job_id'] = ''
			
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
	
	
