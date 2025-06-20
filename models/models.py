#Association tables need to be imported before the 2 table that association table is using 
from .speciesclassification import SpeciesClassification
from .symptomsclassifications import SymptomClassification
from .illnesssymptom import IllnessSymptom
from .illnessclassification import IllnessClassification
from .species import Species
from .classification import Classification
from .symptom import Symptom
from .user import User
from .pet import Pet
from .petsymptom import PetSymptom
from .illness import Illness
from .medication import Medication
from .illnessmedication import IllnessMedication
from .product import Product
from .cart import Cart
from .illnessproduct import IllnessProduct