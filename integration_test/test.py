# -*- coding: utf-8 -*


import pymongo
import pytest
import requests

from bson.json_util import dumps
from test_peuplement import init_db
from pymongo import MongoClient, GEO2D

client = MongoClient('mongodb://localhost:27017/')
db = client['test_chopper_db']
Beers = db.beers
Bars = db.bars
Brass = db.brass

def init_db_test():
    Beers.insert(init_db.initbeers())
    Brass.create_index([("Loc", GEO2D)])
    Brass.insert(init_db.initbrass())
    Bars.create_index([("Loc", GEO2D)])
    Bars.insert(init_db.initbars())

def kill_db():
    Beers.drop()
    Bars.drop()
    Brass.drop()

def test_search_beer_by_name():
    payload = {'newb':'Goudale'}
    r = requests.get('http://localhost:5000/searchbierebyname', params=payload)
    if r.text == "[]" :
        print('- Search beer by name : FAIL')
    else :
        print('- Search beer by name : OK')

def test_search_beer():
    payload = {'newb':'Goudale' , 'type':'Blonde', 'tast':'Classique', 'flav':'Hoûblon, caramel', 'alco':'7,2', 'brass':'Gayant'}
    r = requests.get('http://localhost:5000/searchbiere', params=payload)
    if r.text == "[]" :
        print('- Search beer : FAIL')
    else :
        print('- Search beer : OK')

def test_search_beer_by_brass():
    payload = {'brass':'Achouffe'}
    r = requests.get('http://localhost:5000/searchbierebybrasserie', params=payload)
    if r.text == "[]" :
        print('- Search beer by brass : FAIL')
    else :
        print('- Search beer by brass : OK')

def test_search_beer_by_type():
    payload = {'type':'Blonde'}
    r = requests.get('http://localhost:5000/searchbierebytype', params=payload)
    if r.text == "[]" :
        print('- Search beer by type : FAIL')
    else :
        print('- Search beer by type : OK')

def test_search_brass_by_name():
    payload = {'brass':'Achouffe'}
    r = requests.get('http://localhost:5000/searchbrasseriebyname', params=payload)
    if r.text == "[]" :
        print('- Search brass by name : FAIL')
    else :
        print('- Search brass by name : OK')

def test_search_bar_by_beer():
    payload = {'beer':'Goudale', 'adress':'3 Place de Viarmes Morlaix'}
    r = requests.get('http://localhost:5000/searchbarbybeer', params=payload)
    if r.text == "[]" :
        print('- Search bar by beer : FAIL')
    else :
        print('- Search bar by beer : OK')


        #VARIABLE D'ENVIRONEMENT 

init_db_test()
print('Search test :')
test_search_beer()
test_search_beer_by_name()
test_search_beer_by_brass()
test_search_beer_by_type()
test_search_brass_by_name()
test_search_bar_by_beer()
kill_db()
