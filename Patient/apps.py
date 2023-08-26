from django.apps import AppConfig

import os
import joblib
from django.apps import AppConfig
from django.conf import settings
from joblib import load
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

class PatientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Patient'
    MLFOLDER=os.path.join(BASE_DIR,'models')
    MODEL_FILE=os.path.join(MLFOLDER,'diabetes.joblib')

