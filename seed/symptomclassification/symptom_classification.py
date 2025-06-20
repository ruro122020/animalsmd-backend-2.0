from config import app, db
from models.models import Symptom, Classification, SymptomClassification
from .symptoms_classifications_data import symptoms_classifications_data

#symptoms and classifications id's are being used to store them as foreign keys to symptomclassification association table
def seed_symptom_classification():
  with app.app_context():
    for sypmtom_name, classification_names in symptoms_classifications_data.items():
      symptom = Symptom.query.filter_by(name=sypmtom_name).first()

      #check if symptom id already exist in symptomclassification table
      symptom_in_symptomclassification_table = SymptomClassification.query.filter_by(symptoms_id = symptom.id).first()

      #if symptoms doesn't exist, no classifications will exist 
      if not symptom_in_symptomclassification_table:

        classification_db = []

        for classification_name in classification_names:
          classification = Classification.query.filter_by(classification = classification_name).first()

          classification_db.append(classification)

        for classification in classification_db:
          SymptomClassification.create_row(classification, symptom)
      else:
        #this currently isn't needed, due to working with just 3 classifications for now
        #this is for a future need, if more classifications are added 
        #check is each symptoms has a relation to its appropriate classification
        pass


seed_symptom_classification()