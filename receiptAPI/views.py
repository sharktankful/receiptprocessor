from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import uuid
import math
from datetime import datetime


receipt_data_dict = {}

# Create your views here.


@api_view(['POST'])
@csrf_exempt
def process(request):
    if request.method == 'POST':
        try:
            # STORE JSON RECEIPT IN VARIABLE
            receipt_data = json.loads(request.body)

            # GENERATE UNIQUE ID
            generated_id = str(uuid.uuid4())

            # STORE ID AS KEY AND RECEIPT_DATA AS VALUE IN GLOBAL RECEIPT_DATA_DICT VARIABLE
            receipt_data_dict[generated_id] = receipt_data

            # NEW JSON OBJECT THAT GETS RETURNED AS RESPONSE
            response_data = {"id": generated_id}
            return Response(response_data, status=201)

        # THROWS ERROR IS JSON RECEIPT IS INVALID
        except json.JSONDecodeError:
            return Response({"error": "Invalid Json data"}, status=400)
    else:
        # THROWS ERROR IF REQUEST ANYTHING THAN 'POST'
        return Response({"error": "Method not allowed"}, status=405)


@api_view(['GET'])
@csrf_exempt
def calculate_points(request, id):
    # PUTS DATA OF SPECIFIC ID IN ITS OWN SEPERATE DICTIONARY
    receipt_data = receipt_data_dict.get(str(id))

    if receipt_data:
        point_count = 0
        retailer = str(receipt_data['retailer'])
        total = float(receipt_data['total'])
        items = receipt_data['items']
        purchase_date = receipt_data['purchaseDate']
        purchase_time = receipt_data['purchaseTime']

        # CHECK IF EVERY CHARACTER IS AN ALPHANUMERIC CHARACTER
        for char in retailer:
            if char.isalnum():
                point_count += 1

        # CHECK IF TOTAL IS A ROUND DOLLOR AND IS A MULTIPLE OF 0.25
        if total == int(total):
            point_count += 50

        if total % 0.25 == 0:
            point_count += 25

        # INCREMENTS COUNT BY 5 POINTS FOR EVERY 2 ITEMS IN THE THE ITEMS LIST
        items_points = 5 * (len(items) // 2)
        point_count += items_points

        # IF LENGTH OF ITEM IS MULTIPLE OF 3, PRICE IS MULTIPLIED BY O.2, ITS THEN ROUNDED, AND APPENDED TO COUNT
        for item in items:
            description = item.get('shortDescription').strip()
            description_length = len(description)
            item_price = float(item.get('price'))

            if description_length % 3 == 0:
                added_points = math.ceil(item_price * 0.2)
                point_count += added_points

        # INCREMENT COUNT BY 6 POINTS IF PURCHASE DAY IS AN ODD NUMBER
        purchase_day = int(purchase_date.split('-')[2])
        if purchase_day % 2 == 1:
            point_count += 6

        # IF PURCHASE TIME IS BETWEEN 2PM AND 4PM THEN COUNT IS INCREMENTED BY 10
        start_time = datetime.strptime('14:00', '%H:%M')
        end_time = datetime.strptime('16:00', '%H:%M')
        purchase_time = datetime.strptime(purchase_time, '%H:%M')

        if purchase_time > start_time and purchase_time < end_time:
            point_count += 10

        # RETURNS TOTAL POINTS AS A NEW JSON OBJECT AT THE SPECIFIED ENDPOINT
        response_data = {"points": point_count}
        return Response(response_data, status=200)
    else:
        return Response({"error": "Receipt not found"}, status=404)
