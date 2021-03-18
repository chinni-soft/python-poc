from flask import session, Response, request, jsonify
from flask_classy import FlaskView, route
from models import WhiteboardModel, WhiteboardSchema, db #, WhiteboardTask, WhiteboardTaskSchema
import json
from logger import log

whiteboard_schema = WhiteboardSchema()

class DataView(FlaskView):
    route_base = '/'
 
    @route('/events', methods=['POST'])
    def create_event(self):
        """ Creation of White Board Events """
        try:
            req_data = request.get_json()             #Input POST Data / Payload
            status = req_data.get('status')
            data = whiteboard_schema.load(req_data)
            
            event = WhiteboardModel(data)
            event.save()
            ser_data = whiteboard_schema.dump(event)
            
            Response = {'message': 'Event Created', 'status': '201', 'response': ser_data}
            log.info("Event Created Succesfully --> {}".format(Response))
            return Response
        except Exception as e:
            print("Something Went wrong while creating Event --> ", e)
            log.error("Something Went wrong while creating Event --> {} ".format(e))
            return "Something Went wrong while creating Event --> {} ".format(e)


    @route('/events')
    def events_all(self):
        """ Get all events """
        events = WhiteboardModel.get_all_events()
        ser_events = whiteboard_schema.dump(events, many=True)
        log.info("All Events --> {}".format(ser_events))
        return self.custom_response(ser_events, 200)

    @route('/events/<int:event_id>', methods=['GET'])
    def get_a_event(self, event_id):
        """ Get a single event """
        event = WhiteboardModel.get_one_event(event_id)
        if not event:
            log.info("No Events found for this event id --> {}".format(event_id))
            return self.custom_response({'error': 'Event not found'}, 404)
  
        ser_event = whiteboard_schema.dump(event)
        log.info("Event info --> {}".format(ser_event))
        return self.custom_response(ser_event, 200)


    @route('/events/<int:event_id>', methods=['PUT'])
    def update_a_event(self, event_id):
        """ Update a single event """
        try:
            req_data = request.get_json()
            data = whiteboard_schema.load(req_data, partial=True)
            event = WhiteboardModel.get_one_event(event_id)
            
            if not event:
                log.info("No Event found with this id --> {}".format(event_id))
                return self.custom_response({'error': 'Event not found with this Id'}, 404)
            else:
                event.update(data)
                ser_event = whiteboard_schema.dump(event)
                #print("RES UPDATE", ser_event)
                Response = {'message': 'Event Updated', 'status': '201', 'response': ser_event}
                log.info("Event Updated --> {}".format(Response))
                return Response
        except Exception as e:
            log.info("Something went wrong while updating event --> {}".format(e))
            return "Something went wrong while updating event --> {}".format(e)

      
    def custom_response(self, res, status_code):
        """ Custom Response Function  """
        return Response(
            mimetype="application/json",
            response=json.dumps(res),
            status=status_code
            )