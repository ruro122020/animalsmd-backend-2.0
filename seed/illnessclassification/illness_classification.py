from config import db, app
from models.models import IllnessClassification, Illness, Classification
from .illnesses_classifications_data import illness_classification_data


def seed_illness_classification():
  with app.app_context():
    for classification_name in illness_classification_data:
      #query classification table for classification id 
      classification = Classification.query.filter_by(classification = classification_name).first()
      
      for illness_name in illness_classification_data[classification_name]:
        illness = Illness.query.filter_by(name=illness_name).first()
        print('illness', illness)
        #check if illness exist in illnessesclassifications table
        illness_exist = IllnessClassification.query.filter_by(illness_id = illness.id ).first()
        if not illness_exist:
          #create a row in IllnessClassifications with the illness id and classification id
          # IllnessClassification.create_row(illness, classification)  
          pass

seed_illness_classification()  
