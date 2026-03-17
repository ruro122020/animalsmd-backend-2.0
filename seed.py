#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
import random

# Remote library imports
from faker import Faker

# Local imports
from app import app
from config import db

def clear_database():
  """Delete all data from all tables and restart identity sequences."""
  with app.app_context():
    print("Clearing database...")
    db.session.execute(db.text("TRUNCATE TABLE carts, petsymptoms, pets, users, symptomsclassifications, illnessesproducts, illnessesmedications, illnessessymptoms, illnessesclassifications, speciesclassifications, products, symptoms, medications, illnesses, species, classifications RESTART IDENTITY CASCADE"))
    db.session.commit()
    print("Database cleared.")

if __name__ == '__main__':
  print("Starting seed...")

  clear_database()

  # Base tables (no dependencies)
  print("Seeding classifications...")
  import seed.classification.classification

  print("Seeding species...")
  import seed.species.species

  print("Seeding illnesses...")
  import seed.illness.illness

  print("Seeding medications...")
  import seed.medication.medication

  print("Seeding symptoms...")
  import seed.symptom.symptom

  print("Seeding products...")
  import seed.product.product

  # Association tables (depend on base tables)
  print("Seeding species classifications...")
  import seed.speciesclassification.species_classification

  print("Seeding illness classifications...")
  import seed.illnessclassification.illness_classification

  print("Seeding illness symptoms...")
  import seed.illnesssymptom.illness_symptom

  print("Seeding illness medications...")
  import seed.illnessmedication.illness_medication

  print("Seeding illness products...")
  import seed.illnessproduct.illness_product

  print("Seeding symptom classifications...")
  import seed.symptomclassification.symptom_classification

  # User-dependent tables
  print("Seeding users...")
  import seed.user.user

  print("Seeding pets...")
  import seed.pet.pet

  print("Seeding pet symptoms...")
  import seed.petsymptom.pet_symptom

  print("Seeding cart...")
  import seed.cart.cart

  print("Seeding complete.")
