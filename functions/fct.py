# -*- coding: utf-8 -*

import googlemaps
import math
import json
import pymongo

from flask import Response
from bson.json_util import dumps
from bson.son import SON
from datetime import datetime
from math import *
from pymongo import MongoClient, GEO2D
from db import connect


Beers = connect.db.beers
Brass = connect.db.brass
Bars = connect.db.bars

R = 6367445

gmaps = googlemaps.Client(key='AIzaSyDW0GVTyrOEkMNFjX8AvfEgjP41X75NHb8')

# Function returning the coord for an adresse
# Fonction retournant les coordonnées pour l'adresse donnée
def figeo(adresse):
    """Function returning the coord for the adresse give in args"""
    cord = find_loc(adresse)
    document = Bars.find({"Loc":{"$near":[cord[0],cord[1]]}},{"_id": 0})
    a= list(document)
    a = fctsortbydistance(list=a,coord=cord)
    return returning(a)

def find_loc(adresse):
    geocode_result = gmaps.geocode(adresse)
    for result in geocode_result:
        try:
            coord = result['geometry']['location']
        except KeyError:
            coord = None
    cord =[coord["lat"],coord["lng"]]
    return cord

def test_presence(user , collection):
    test = collection.find({"Nom":user} , {"_id":0})
    json2 = dumps(test)
    if json2 == "[]" :
        return False
    else :
        return True

# Function returning the coord for an adresse
# Fonction retournant les coordonnées pour l'adresse donnée
def figeo2(lat,lon,beer):
    """Function returning the coord for the adresse guve in args"""
    
    cord = [float(lat),float(lon)];
    document = Bars.find({"$and": [{"Loc":SON([("$near",[cord[1],cord[0]]),("$maxDistance",993)])},{"Bieres":beer}]},{"_id": 0})
    a= list(document)
    print(document)
    print(a)
    a = fctprescaledist(list=a,coord=cord)
    a = fctsortbydistance(list=a,coord=cord)
    return returning(a)

def distance(lata,lona,latb,lonb):
    ra = (lata*2*pi)/360
    rb = (latb*2*pi)/360
    rc = (lona*2*pi)/360
    rd = (lonb*2*pi)/360
    d = R*acos(sin(ra)*sin(rb)+cos(ra)*cos(rb)*cos(abs(rd-rc)))
    return d

def fctprescaledist(list,coord):
    b = len(list)
    i = 0
    while i<b :
        document0=list[i]["Loc"]
        document1=list[i]
        lng0 = document0[0]
        lat0 = document0[1]
        dist = distance(coord[0],coord[1],lat0,lng0)
        print(dist)
        if dist >= 3000000 :
            del list[i]
            b -=1
        else:
            i += 1
    return list

def fctsortbydistance(list,coord):
    b= len(list)
    i =0
    i1 =0
    while i<b:
        document0=list[i]["Loc"]
        document1=list[i]
        lng0 = document0[0]
        lat0 = document0[1]
        resultat0 = gmaps.distance_matrix((coord[0],coord[1]),(lat0,lng0))
        distance0 = resultat0["rows"][0]["elements"][0]["distance"]["text"]
        value0 = resultat0["rows"][0]["elements"][0]["distance"]["value"]
        list[i]["Distance"] = distance0
        if value0 >= 3000000 :
            break
        i+= 1
    list = sorted(list, key=fctSortDict,reverse=False)
    return list

def fctSortDict(value):
    return value['Distance']

def returning(data):
    jumps = dumps(data)
    resp = Response(jumps, status=200, mimetype='application/json')
    return resp

def returningall(mess, stat):
    jumps = dumps(mess)
    resp = Response(jumps, status=stat, mimetype='application/json')
    return resp

def searchbarbybeers(beer):
    data = {}
    data = Bars.find({"Bieres":beer},{"_id":0})
    return data
