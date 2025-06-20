#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
import random
# Remote library imports
from faker import Faker

# Local imports
from app import app
from config import db


from seed import seed_medications_table

if __name__ == '__main__':
  pass
  # fake = Faker()
  # with app.app_context():
  #   print("Starting seed...")
  #   # Seed code goes here!
  #   print('Deleting all records...')
  #   User.query.delete()

#USERS FAKE DATA
    # users = []
    # usernames = []
    # for i in range(5):
    #   username = fake.first_name()
    #   email = f'{fake.last_name()}@{fake.domain_name()}'
    #   #this while is to check if a username already exist
    #   while username in usernames:
    #       username = fake.first_name()
    #   usernames.append(username)
      
    #   user = User(
    #       name=fake.name(),
    #       username=username,
    #       email=email
    #       )
      
    #   user.password_hash = user.username + 'password'

    #   users.append(user)
    
    # db.session.add_all(users)
    # db.session.commit()

#SPECIES 


#CLASSIFICATIONS
    # classifications = Classification(classification='mammal')
    # db.session.add(classifications)
    # db.session.commit()

    # classifications = Classification(classification='reptile')
    # db.session.add(classifications)
    # db.session.commit()

#SPECIES-CLASSIFICATION
    # species_classification = SpeciesClassification(classification_id=1, species_id=2)
    # db.session.add(species_classification)
    # db.session.commit()

print('Complete.')