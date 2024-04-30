from django.db import models
"""import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
cred = credentials.Certificate(r"C:\Users\johim\Desktop\Farmsense\privatekey.json")
firebase_admin.initialize_app(cred)

db= firestore.client()"""
# Create your models here.

"""class Plant(models.Model):
    plant_ref=db.collection('plant_suggestions').get()
    for plant_data in plant_ref:
        plants=plant_data.to_dict()
        key=plants.id
        plant=plants.get('plant')
        createdAt=plants.get('createdAt')
        createdBy=plants.get('createdBy')
    #return render(request, 'plants.html',{"id":key,"name":plant,"createdAt":createdAt,"createdBY": createdBy})"""