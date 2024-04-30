from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
#from django.views.decorators.http import require_POST
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
cred = credentials.Certificate(r"C:\Users\johim\Desktop\Farmsense\privatekey.json")
firebase_admin.initialize_app(cred)

db= firestore.client()

# current datetime
current_datetime = datetime.datetime.now()

# Create your views here.

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Initialize Firestore client
        #db = firestore.client()
        

        # Query Firestore for user with the provided email
        query = db.collection('admin').where('email', '==', email).get()

        for admin_doc in query:
            admin_data=admin_doc.to_dict()
            #check password if the provided email matches the firestore
            if admin_data['password'] == password:
                #username=admin_data.get('username')
                return render(request, 'admin.html')
        return render(request, 'login.html',{'error': 'Invalid email or password'})
    else:
        return redirect('/login')



def ad(request):
    return render(request, 'admin.html')


def plants(request):
    plant_ref = db.collection('plant_suggestion')

    query = plant_ref.stream()

    plant_data_list = []
    for plant_data in query:
        plant_id = plant_data.id
    # Convert document data to a Python dictionary
        plants = plant_data.to_dict()
    
    # Access individual fields from the document data
        plant = plants.get('plant')
        potassium = plants.get('potassium')
        phosphorus = plants.get('phosphorus')
        nitrogen = plants.get('nitrogen')
        moisture = plants.get('moisture')
        humidity = plants.get('humidity')
        fertilizer = plants.get('fertilizer')
        soil = plants.get('soil_type')
        temperature = plants.get('temperature')
        createdAt = plants.get('createdAt')
        updatedAt = plants.get('updatedAt')
        plant_data_list.append({'name' : plant,
                                'createdAt' : createdAt,
                                'updatedAt' : updatedAt,
                                'potassium' : potassium,
                                'nitrogen' : nitrogen,
                                'phosphorus' : phosphorus,
                                'moisture' : moisture,
                                'temperature' : temperature,
                                'humidity' : humidity,
                                'fertilizer' : fertilizer,
                                'soil' : soil,
                                'id': plant_id})

    return render(request,'plants.html',{'plant_data': plant_data_list})


def create_plant(request):
    #if request.method == 'POST':
    return render(request, 'create_plants.html')



def create_plant_view(request):
    if request.method == 'POST':
        document_id = request.POST.get('plant_id')
        plant = request.POST.get('plant')
        fertilizer = request.POST.get('fertilizer')
        soil = request.POST.get('soil')
        temperature = request.POST.get('temperature')
        moisture = request.POST.get('moisture')
        humidity = request.POST.get('humidity')
        potassium = request.POST.get('potassium')
        nitrogen = request.POST.get('nitrogen')
        phosphorus = request.POST.get('phosphorus')
        
        
        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime
        createdAt = firestore.SERVER_TIMESTAMP
        updatedAt = firestore.SERVER_TIMESTAMP

        data = {'plant' : plant,
                'createdAt' : createdAt,
                'updatedAt' : updatedAt,
                'soil_type' : soil,
                'potassium' : potassium,
                'nitrogen' : nitrogen,
                'phosphorus' : phosphorus,
                'moisture' : moisture,
                'temperature' : temperature,
                'humidity' : humidity,
                'fertilizer' : fertilizer,
                
        }

        doc=db.collection('plant_suggestion').document()
        doc.set(data)
        return redirect("/plants")

def edit_plant(request):
    if request.method == 'POST':
        document_id = request.POST.get('plant_id')
        # Delete document from Firestore
        # print(document_id)
        plant_ref = db.collection('plant_suggestion').document(document_id).get()
        

        plant_data_list = []
    
            
        plants = plant_ref.to_dict()
        # Access individual fields from the document data
        plant = plants.get('plant')
        potassium = plants.get('potassium')
        phosphorus = plants.get('phosphorus')
        nitrogen = plants.get('nitrogen')
        moisture = plants.get('moisture')
        humidity = plants.get('humidity')
        fertilizer = plants.get('fertilizer')
        soil = plants.get('soil_type')
        temperature = plants.get('temperature')
        #createdAt = plants.get('createdAt')
        #updatedAt = plants.get('updatedAt')

        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime

        updatedAt = firestore.SERVER_TIMESTAMP
        
        plant_data_list.append({'name' : plant,
                                'updatedAt' : updatedAt,
                                'potassium' : potassium,
                                'nitrogen' : nitrogen,
                                'phosphorus' : phosphorus,
                                'moisture' : moisture,
                                'temperature' : temperature,
                                'humidity' : humidity,
                                'fertilizer' : fertilizer,
                                'soil' : soil,
                                'id' : document_id,
                                })

        return render(request, 'edit_plants.html' ,{'plant_data': plant_data_list})

def update_plant(request):
    if request.method == 'POST':
        document_id = request.POST.get('plant_id')
        plant = request.POST.get('plant')
        fertilizer = request.POST.get('fertilizer')
        soil = request.POST.get('soil')
        temperature = request.POST.get('temperature')
        moisture = request.POST.get('moisture')
        humidity = request.POST.get('humidity')
        potassium = request.POST.get('potassium')
        nitrogen = request.POST.get('nitrogen')
        phosphorus = request.POST.get('phosphorus')
        
        """datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        createdAt = datetime"""
        """updatedAt = ""
        
        'updatedAt' : updatedAt,"""

        updatedAt = firestore.SERVER_TIMESTAMP
        data = {'plant' : plant,
                'soil_type' : soil,
                'potassium' : potassium,
                'nitrogen' : nitrogen,
                'phosphorus' : phosphorus,
                'moisture' : moisture,
                'temperature' : temperature,
                'humidity' : humidity,
                'fertilizer' : fertilizer,
                'updatedAt' : updatedAt,
        }

        doc=db.collection('plant_suggestion').document(document_id)
        doc.update(data)
        return redirect("/plants")


def delete_plant(request):
    if request.method == 'POST':
        document_id = request.POST.get('plant_id')
        # Delete document from Firestore
        
        db.collection('plant_suggestion').document(document_id).delete()
        
        return redirect("/plants")
        # return JsonResponse({'message': 'Document deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def fertilizers(request):
    fertilizer_ref = db.collection('fertilizer_suggestion')

    query = fertilizer_ref.stream()

    fertilizer_data_list = []
    for fertilizer_data in query:
        fertilizer_id = fertilizer_data.id
    # Convert document data to a Python dictionary
        fertilizers = fertilizer_data.to_dict()
    
    # Access individual fields from the document data
        fertilizer = fertilizers.get('fertilizer')
        potassium = fertilizers.get('potassium')
        phosphorus = fertilizers.get('phosphorus')
        nitrogen = fertilizers.get('nitrogen')
        moisture = fertilizers.get('moisture')
        humidity = fertilizers.get('humidity')
        crop = fertilizers.get('crop_type')
        soil = fertilizers.get('soil_type')
        temperature = fertilizers.get('temperature')
        createdAt = fertilizers.get('createdAt')
        updatedAt = fertilizers.get('updatedAt')
        fertilizer_data_list.append({'name' : fertilizer,
                                'createdAt' : createdAt,
                                'updatedAt' : updatedAt,
                                'potassium' : potassium,
                                'nitrogen' : nitrogen,
                                'phosphorus' : phosphorus,
                                'moisture' : moisture,
                                'temperature' : temperature,
                                'humidity' : humidity,
                                'crop' : crop,
                                'soil' : soil,
                                'id': fertilizer_id})

    return render(request, 'fertilizers.html',{"fertilizer_data":fertilizer_data_list})


def create_fertilizer(request):
    #if request.method == 'POST':
    return render(request, 'create_fertilizers.html')



def create_fertilizer_view(request):
    if request.method == 'POST':
        fertilizer = request.POST.get('fertilizer')
        crop = request.POST.get('crop')
        soil = request.POST.get('soil')
        temperature = request.POST.get('temperature')
        moisture = request.POST.get('moisture')
        humidity = request.POST.get('humidity')
        potassium = request.POST.get('potassium')
        nitrogen = request.POST.get('nitrogen')
        phosphorus = request.POST.get('phosphorus')
        
        
        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime
        createdAt = firestore.SERVER_TIMESTAMP
        updatedAt = firestore.SERVER_TIMESTAMP

        data = {'fertilizer' : fertilizer,
                'createdAt' : createdAt,
                'updatedAt' : updatedAt,
                'soil_type' : soil,
                'potassium' : potassium,
                'nitrogen' : nitrogen,
                'phosphorus' : phosphorus,
                'moisture' : moisture,
                'temperature' : temperature,
                'humidity' : humidity,
                'crop_type' : crop,
                
        }

        doc=db.collection('fertilizer_suggestion').document()
        doc.set(data)
        return redirect("/fertilizers")

def edit_fertilizer(request):
    if request.method == 'POST':
        document_id = request.POST.get('fertilizer_id')
        # Delete document from Firestore
        # print(document_id)
        fertilizer_ref = db.collection('fertilizer_suggestion').document(document_id).get()
        

        fertilizer_data_list = []
    
            
        fertilizers = fertilizer_ref.to_dict()
        # Access individual fields from the document data
        crop = fertilizers.get('crop_type')
        soil = fertilizers.get('soil_type')
        fertilizer = fertilizers.get('fertilizer')
        potassium = fertilizers.get('potassium')
        phosphorus = fertilizers.get('phosphorus')
        nitrogen = fertilizers.get('nitrogen')
        moisture = fertilizers.get('moisture')
        humidity = fertilizers.get('humidity')
        temperature = fertilizers.get('temperature')
        #createdAt = fertilizer.get('createdAt')
        #updatedAt = fertilizers.get('updatedAt')

        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime

        updatedAt = firestore.SERVER_TIMESTAMP
        fertilizer_data_list.append({'name' : fertilizer,
                                'updatedAt' : updatedAt,
                                'potassium' : potassium,
                                'nitrogen' : nitrogen,
                                'phosphorus' : phosphorus,
                                'moisture' : moisture,
                                'temperature' : temperature,
                                'humidity' : humidity,
                                'crop' : crop,
                                'soil' : soil,
                                'id' : document_id,
                                })

        return render(request, 'edit_fertilizers.html' ,{'fertilizer_data': fertilizer_data_list})

def update_fertilizer(request):
    if request.method == 'POST':
        document_id = request.POST.get('fertilizer_id')
        crop = request.POST.get('crop')
        fertilizer = request.POST.get('fertilizer')
        soil = request.POST.get('soil')
        temperature = request.POST.get('temperature')
        moisture = request.POST.get('moisture')
        humidity = request.POST.get('humidity')
        potassium = request.POST.get('potassium')
        nitrogen = request.POST.get('nitrogen')
        phosphorus = request.POST.get('phosphorus')
        
        """datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        createdAt = datetime"""
        """updatedAt = ""
        
        'updatedAt' : updatedAt,"""

        updatedAt = firestore.SERVER_TIMESTAMP
        data = {'fertilizer' : fertilizer,
                'soil_type' : soil,
                'potassium' : potassium,
                'nitrogen' : nitrogen,
                'phosphorus' : phosphorus,
                'moisture' : moisture,
                'temperature' : temperature,
                'humidity' : humidity,
                'crop_type' : crop,
                'updatedAt' : updatedAt,
        }

        doc=db.collection('fertilizer_suggestion').document(document_id)
        doc.update(data)
        return redirect("/fertilizers")


def delete_fertilizer(request):
    if request.method == 'POST':
        document_id = request.POST.get('fertilizer_id')
        # Delete document from Firestore
        
        db.collection('fertilizer_suggestion').document(document_id).delete()
        
        return redirect("/fertilizers")
        # return JsonResponse({'message': 'Document deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def diseases(request):
    disease_ref = db.collection('disease')

    query = disease_ref.stream()

    disease_data_list = []
    for disease_data in query:
        disease_id = disease_data.id
    # Convert document data to a Python dictionary
        diseases = disease_data.to_dict()
        # Access individual fields from the document data
        disease = diseases.get('name')
        cause = diseases.get('cause')
        status = diseases.get('status')
        visibility = diseases.get('visibility')
        reference = diseases.get('reference')
        remedies = diseases.get('remedies')
        createdAt = diseases.get('createdAt')
        updatedAt = diseases.get('updatedAt')
        disease_data_list.append({'name' : disease,
                                  'cause' : cause,
                                  'status' : status,
                                  'visibility' : visibility,
                                  'reference' : reference,
                                  'remedies' : remedies,
                                  'createdAt' : createdAt,
                                  'updatedAt' : updatedAt,
                                  'id' : disease_id})
    return render(request, 'diseases.html',{"disease_data":disease_data_list})

def create_disease(request):

    return render(request, 'create_diseases.html')



def create_disease_view(request):
    if request.method == 'POST':
        disease = request.POST.get('disease')
        cause = request.POST.get('cause')
        status = request.POST.get('status')
        visibility = request.POST.get('visibility')
        references = request.POST.get('reference')
        remedie = request.POST.get('remedies')
        
        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime
        createdAt = firestore.SERVER_TIMESTAMP
        updatedAt = firestore.SERVER_TIMESTAMP

        value_ref = references.split(',')
        value_rem = remedie.split(',')
        remedies = [value.strip() for value in value_rem]
        reference = [value.strip() for value in value_ref]



        data = {'name' : disease,
                'cause' : cause,
                'status' : status,
                'visibility' : visibility,
                'reference' : reference,
                'remedies' : remedies,
                'createdAt' : createdAt,
                'updatedAt' : updatedAt,
        }

        doc=db.collection('disease').document()
        doc.set(data)
        return redirect("/diseases")

def edit_disease(request):
    if request.method == 'POST':
        document_id = request.POST.get('disease_id')
        # Delete document from Firestore
        # print(document_id)
        disease_ref = db.collection('disease').document(document_id).get()
        

        disease_data_list = []
    
            
        diseases = disease_ref.to_dict()
        # Access individual fields from the document data
        disease = diseases.get('name')
        cause = diseases.get('cause')
        status = diseases.get('status')
        visibility = diseases.get('visibility')
        references = diseases.get('reference')
        remedie = diseases.get('remedies')

        remedies = ', '.join(str(item) for item in remedie)
        reference = ', '.join(str(item) for item in references)

        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime

        updatedAt = firestore.SERVER_TIMESTAMP

        disease_data_list.append({'name' : disease,
                                  'cause' : cause,
                                  'status' : status,
                                  'visibility' : visibility,
                                  'reference' : reference,
                                  'remedies' : remedies,
                                  'updatedAt' : updatedAt,
                                  'id' : document_id,
                                  })

        return render(request, 'edit_diseases.html' ,{'disease_data': disease_data_list})

def update_disease(request):
    if request.method == 'POST':
        document_id = request.POST.get('disease_id')
        disease = request.POST.get('disease')
        cause = request.POST.get('cause')
        status = request.POST.get('status')
        visibility = request.POST.get('visibility')
        references = request.POST.get('reference')
        remedie = request.POST.get('remedies')

        """datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        createdAt = datetime"""
        """updatedAt = ""
        
        'updatedAt' : updatedAt,"""

        updatedAt = firestore.SERVER_TIMESTAMP

        value_ref = references.split(',')
        value_rem = remedie.split(',')
        remedies = [value.strip() for value in value_rem]
        reference = [value.strip() for value in value_ref]

        data = {'name' : disease,
                'cause' : cause,
                'status' : status,
                'visibility' : visibility,
                'reference' : reference,
                'remedies' : remedies,
                'updatedAt' : updatedAt,
        }

        doc=db.collection('disease').document(document_id)
        doc.update(data)
        return redirect("/diseases")


def delete_disease(request):
    if request.method == 'POST':
        document_id = request.POST.get('disease_id')
        # Delete document from Firestore
        
        db.collection('disease').document(document_id).delete()
        
        return redirect("/diseases")
        # return JsonResponse({'message': 'Document deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})



def soils(request):
    soil_ref = db.collection('soil_precipitate')

    query = soil_ref.stream()

    soil_data_list = []
    for soil_data in query:
        soil_id = soil_data.id
    # Convert document data to a Python dictionary
        soils = soil_data.to_dict()
        # Access individual fields from the document data
        soil = soils.get('type')
        reference = soils.get('reference')
        procedure = soils.get('procedure')
        createdAt = soils.get('createdAt')
        updatedAt = soils.get('updatedAt')
        soil_data_list.append({'name' : soil,
                               'reference' : reference,
                               'procedure' : procedure,
                               'createdAt' : createdAt,
                               'updatedAt' : updatedAt,
                               'id' : soil_id})

    return render(request, 'soils.html', {"soil_data":soil_data_list})


def create_soil(request):

    return render(request, 'create_soils.html')



def create_soil_view(request):
    if request.method == 'POST':
        soil = request.POST.get('soil')
        references = request.POST.get('reference')
        procedures = request.POST.get('procedure')
        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime
        createdAt = firestore.SERVER_TIMESTAMP
        updatedAt = firestore.SERVER_TIMESTAMP
        value_ref = references.split(',')
        value_pro = procedures.split(',')
        procedure = [value.strip() for value in value_pro]
        reference = [value.strip() for value in value_ref]
        data = {'type' : soil,
                'reference' : reference,
                'procedure' : procedure,
                'createdAt' : createdAt,
                'updatedAt' : updatedAt,
        }

        doc=db.collection('soil_precipitate').document()
        doc.set(data)
        return redirect("/soils")

def edit_soil(request):
    if request.method == 'POST':
        document_id = request.POST.get('soil_id')
        # Delete document from Firestore
        # print(document_id)
        soil_ref = db.collection('soil_precipitate').document(document_id).get()
        

        soil_data_list = []
    
            
        soils = soil_ref.to_dict()
        # Access individual fields from the document data
        soil = soils.get('type')
        references = soils.get('reference')
        procedures = soils.get('procedure')
        
        procedure = ', '.join(str(item) for item in procedures)
        reference = ', '.join(str(item) for item in references)
        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime


        soil_data_list.append({'name' : soil,
                               'reference' : reference,
                               'procedure' : procedure,
                               'id' : document_id
                               })

        return render(request, 'edit_soils.html' ,{'soil_data': soil_data_list})

def update_soil(request):
    if request.method == 'POST':
        document_id = request.POST.get('soil_id')
        soil = request.POST.get('soil')
        references = request.POST.get('reference')
        procedures = request.POST.get('procedure')

        """datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        createdAt = datetime"""
        """updatedAt = ""
        
        'updatedAt' : updatedAt,"""
        value_ref = references.split(',')
        value_pro = procedures.split(',')
        procedure = [value.strip() for value in value_pro]
        reference = [value.strip() for value in value_ref]
        updatedAt = firestore.SERVER_TIMESTAMP
        data = {'type' : soil,
                'reference' : reference,
                'procedure' : procedure,
                'updatedAt' : updatedAt,
        }

        doc=db.collection('soil_precipitate').document(document_id)
        doc.update(data)
        return redirect("/soils")


def delete_soil(request):
    if request.method == 'POST':
        document_id = request.POST.get('soil_id')
        # Delete document from Firestore
        
        db.collection('soil_precipitate').document(document_id).delete()
        
        return redirect("/soils")
        # return JsonResponse({'message': 'Document deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def devices(request):
    device_ref = db.collection('device')

    query = device_ref.stream()

    device_data_list = []
    for device_data in query:
        device_id = device_data.id
    # Convert document data to a Python dictionary
        devices = device_data.to_dict()
    
    # Access individual fields from the document data
        name = devices.get('name')
        geolocation = devices.get('geolocation')
        mac_address = devices.get('mac_address')
        description = devices.get('description')
        rainfall = devices.get('rainfall')
        status = devices.get('status')
        moisture = devices.get('moisture')
        humidity = devices.get('humidity')
        temperature = devices.get('temperature')
        createdAt = devices.get('createdAt')
        updatedAt = devices.get('updatedAt')
        device_data_list.append({'name' : name,
                                'createdAt' : createdAt,
                                'updatedAt' : updatedAt,
                                'geolocation' : geolocation,
                                'description' : description,
                                'mac_address' : mac_address,
                                'moisture' : moisture,
                                'temperature' : temperature,
                                'humidity' : humidity,
                                'rainfall' : rainfall,
                                'status' : status,
                                'id': device_id})

    return render(request,'devices.html',{'device_data': device_data_list})


def create_device(request):
    #if request.method == 'POST':
    return render(request, 'create_devices.html')


def create_device_view(request):
    if request.method == 'POST':
        name = request.POST.get('device')
        geolocation = request.POST.get('geolocation')
        mac_address = request.POST.get('mac_address')
        description = request.POST.get('description')
        rainfall = request.POST.get('rainfall')
        status = request.POST.get('status')
        moisture =request.POST.get('moisture')
        humidity =request.POST.get('humidity')
        temperature =request.POST.get('temperature')
        
        
        #datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        #createdAt = datetime
        createdAt = firestore.SERVER_TIMESTAMP
        updatedAt = firestore.SERVER_TIMESTAMP

        data = {'name' : name,
                'createdAt' : createdAt,
                'updatedAt' : updatedAt,
                'geolocation' : geolocation,
                'description' : description,
                'mac_address' : mac_address,
                'moisture' : moisture,
                'temperature' : temperature,
                'humidity' : humidity,
                'rainfall' : rainfall,
                'status' : status,
                
        }

        doc=db.collection('device').document()
        doc.set(data)
        return redirect("/devices")

def edit_device(request):
    if request.method == 'POST':
        document_id = request.POST.get('device_id')
        # Delete document from Firestore
        # print(document_id)
        device_ref = db.collection('device').document(document_id).get()
        

        device_data_list = []
    
            
        devices = device_ref.to_dict()
        # Access individual fields from the document data
        name = devices.get('name')
        geolocation = devices.get('geolocation')
        mac_address = devices.get('mac_address')
        description = devices.get('description')
        rainfall = devices.get('rainfall')
        status = devices.get('status')
        moisture = devices.get('moisture')
        humidity = devices.get('humidity')
        temperature = devices.get('temperature')
        device_data_list.append({'name' : name,
                                'geolocation' : geolocation,
                                'description' : description,
                                'mac_address' : mac_address,
                                'moisture' : moisture,
                                'temperature' : temperature,
                                'humidity' : humidity,
                                'rainfall' : rainfall,
                                'status' : status,
                                'id': document_id})

        return render(request, 'edit_devices.html' ,{'device_data': device_data_list})

def update_device(request):
    if request.method == 'POST':
        document_id = request.POST.get('device_id')
        name = request.POST.get('device')
        geolocation = request.POST.get('geolocation')
        mac_address = request.POST.get('mac_address')
        description = request.POST.get('description')
        rainfall = request.POST.get('rainfall')
        status = request.POST.get('status')
        moisture =request.POST.get('moisture')
        humidity =request.POST.get('humidity')
        temperature =request.POST.get('temperature')
        
        """datetime = current_datetime.strftime("%B %d, %Y, %I:%M %p")
        createdAt = datetime"""
        """updatedAt = ""
        
        'updatedAt' : updatedAt,"""

        updatedAt = firestore.SERVER_TIMESTAMP
        data = {'name' : name,
                'updatedAt' : updatedAt,
                'geolocation' : geolocation,
                'description' : description,
                'mac_address' : mac_address,
                'moisture' : moisture,
                'temperature' : temperature,
                'humidity' : humidity,
                'rainfall' : rainfall,
                'status' : status,
                'updatedAt' : updatedAt,
        }

        doc=db.collection('device').document(document_id)
        doc.update(data)
        return redirect("/devices")
    
import os

def delete_device(request):
    if request.method == 'POST':
        document_id = request.POST.get('device_id')
        # Delete document from Firestore
        
        db.collection('device').document(document_id).delete()
        
        return redirect("/devices")
        # return JsonResponse({'message': 'Document deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
from scipy.stats import mode
import pandas as pd
import numpy as np
import joblib

def plant_recommender(n, p, k, temp, humidity, ph, rainfall):

    """
    This function accepts the parameter and suggest the plant
    to be planted to give good yield based on the factors
    
    ------------------------------------------------------------
    The NPK, pH, rainfall should be taken the most recent value,
    if and only if the system is not allowed to collect current
    value from the environment
    ------------------------------------------------------------

    :param n: The value of nitrogen - percentage / weight
    :param p: The value of phosporous - percentage / weight
    :param k: The value of potassium - percentage / weight
    :param temp: The current temperature - celsius
    :param humidity: The current value of humidity - percentage
    :param ph: The value of ph - unitless
    :param rainfall: The value of rainfall - mm

    :return prediction: The crop suggestion (actual name of the crop)
    """
    
    # Load the saved models
    svc_model = joblib.load('admin/model/svc_model.pkl')
    dt_model = joblib.load('admin/model/decision_tree_model.pkl')
    gbm_model = joblib.load('admin/model/gbm_model.pkl')
    lr_model = joblib.load('admin/model/lr_model.pkl')
    rf_model = joblib.load('admin/model/rf_model.pkl')

    
    # Current Data from IoT

    current_data = np.array(
        [
            [
                91,         # N
                12,         # P
                46,         # K
                24.644585,  # Temp
                85.499382,  # Humidity
                6.343943,   # pH
                48.312190   # Rainfall - APi Call data
            ]
        ]
    )
    
    #current_data = np.array([[n, p, k, temp, humidity, ph, rainfall]])
    
    # Define column names for the DataFrame
    columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Convert NumPy array to DataFrame
    current_df = pd.DataFrame(current_data, columns=columns)
    
    
    # Make predictions using the loaded models
    svc_predictions = svc_model.predict(current_df)
    dt_predictions = dt_model.predict(current_df)
    gbm_predictions = gbm_model.predict(current_df)
    lr_predictions = lr_model.predict(current_df)
    rf_predictions = rf_model.predict(current_df)
    
    # Append and take mode
    prediction = mode(np.array([svc_predictions, dt_predictions, gbm_predictions, lr_predictions, rf_predictions]))[0][0][0]
    return prediction

print(os.getcwd())
print(plant_recommender(5, 3, 6, 7, 8, 2, 1))


