from flask import request, session
from flask_restful import Resource
from config import api, db

class EbayNotifications(Resource):
  def post(self):
      notification_data = request.json  # Assuming eBay sends JSON data
      # Process the notification_data here
      
      #Log the notification
      print("Received eBay notification:", notification_data)
      
      #Reply back with the challenge code (if required)
      if 'challenge_code' in notification_data:
          return {'challenge_code': notification_data['challenge_code']}

      # Respond with a success message
      return {'message': 'Notification received successfully'}, 200


api.add_resource(EbayNotifications, '/ebay/notifications/<str:notification>', endpoint='ebay_notifications')