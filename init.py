# -*- coding: utf-8 -*

# Document created by :
# - Baptiste LANOUE
# - Valentin ALVES
# - Valentin VERVEUR
# Date of creation : 20/11/2018
# Date of the latest modif : 20/11/2018

# Initialisation of the API

# |---------------------------------| IMPORT |---------------------------------|

import json
import pymongo
import math
from flask import Flask, redirect, url_for, request, render_template, Response, make_response, jsonify
from pymongo import MongoClient, GEO2D
from bson.json_util import dumps

from db import connect
from functions import fct

# |-----------------------------| CONFIG MONGO |-------------------------------|

# Configuration of the connection whit the database
# Configuration de la connection à la database
app = Flask(__name__)
Beers = connect.db.beers
Brass = connect.db.brass
Bars = connect.db.bars

# |-----------------------| KILL THE BEER COLLECTION |-------------------------|

@app.route('/killbeers', methods=['GET'])
def kill_beers():
    Beers.drop()
    return "Collection droped"

# |-----------------------| KILL THE BRASS COLLECTION |------------------------|

@app.route('/killbrass', methods=['GET'])
def kill_brass():
    Brass.drop()
    return "Collection droped"

# |------------------------| KILL THE BAR COLLECTION |-------------------------|

@app.route('/killbars', methods=['GET'])
def kill_bars():
    Bars.drop()
    return "Collection droped"

# |---------------------------------| INDEX |----------------------------------|

# Root for the index page
# Chemin route vers la page d'index
@app.route('/', methods=['GET'])
def home():
    """Root for the index page"""
    return render_template('index.html')

# |---------------------------| ADD OF RESSOURCE |-----------------------------|

# Root to the html form of the add of a new beer
# Chemin route vers le formulaire html d'ajout d'une bière à la collection
@app.route('/NewBeerForm')
def NBF():
    """Root to the html form of the add of a new beer"""
    return render_template('new_beer_form.html')

# Root to the html form of the add of a new bar
# Chemin route vers le formulaire html d'ajout d'un bar à la collection
@app.route('/NewBarForm')
def NBAF():
    """Root to the html form of the add of a new bar"""
    return render_template('new_bar_form.html')

# Double request root of adding new bar to the collection whit a "already
# exist" test
# Chemin route d'ajout d'un bar à la collection comprennant un test de
# présence à double requête (get + post)
@app.route('/newbar', methods=['POST', 'GET'])
def newbar():
    """Root to add a new beer, use POST to add"""
    if request.method == 'POST':
        # Recuperation of the data in the form
        # Récupération des informations depuis le formulaire
        name = request.form['newb']
        adresse = request.form['adres']
        country = request.form['count']
        beers = request.form['beers']
        pbeers = request.form['beersp']
        botbeers = request.form['beersb']
        schedule1 = request.form['sched1']
        schedule2 = request.form['sched2']
        schedule3 = request.form['sched3']
        schedule4 = request.form['sched4']
        schedule5 = request.form['sched5']
        schedule6 = request.form['sched6']
        schedule7 = request.form['sched7']
        # Collection of the geo data
    	geocode_result = gmaps.geocode(adresse)
    	for result in geocode_result:
    		try:
    			coord = result['geometry']['location']
    		except KeyError:
    			coord = None
    	lat = coord["lat"]
    	lng = coord["lng"]
    	# db.geo.insert({"adresse":geo,"loc": [lng,lat]})
        # Test of presence of the resource in the collection
        # Test de présence dans la collection
        test = Bars.find({"Nom":name, "Adresse":adresse, "Pays":country},
                          {"_id":0})
        json2 = dumps(test)
        if  json2 != "[]":
		          return redirect(url_for('fail_new_bar', name=name))
        else:
		          Bars.insert({"Nom":name, "Adresse":adresse, "Pays":country,
                          "Bières":beers, "Bieres Pressions":pbeers,
                          "Bieres Bouteilles":botbeers, "Loc": [lng,lat]})
		          return redirect(url_for('success_new_bar', name=name))
    else:
        name = request.get['newb']
        adresse = request.get['adres']
        country = request.get['count']
        beers = request.get['beers']
        pbeers = request.get['beersp']
        botbeers = request.get['beersb']
        schedule = request.get['sched']
        return redirect(url_for('success_new_bar', name=name))

@app.route('/fail_new_bar/<name>')
def fail_new_bar(name):
    """Root use to return the indication that the ressource already exist in
    the Collection
    """
    return 'Doublon, le bar : %s' %name + ' existe deja'

# Root for the success add of a bar to the collection
# Chemin route renvoyant le succes de l'ajout d'un bar à la collection
@app.route('/success_new_bar/<name>')
def success_new_bar(name):
    """Root returning the sucess of adding a bar"""
    return 'Nom ddu bar %s' % name + ' a bien ete ajoute'

# Double request root of adding new beer to the collection whit a "already
# exist" test
# Chemin route d'ajout d'une bière à la collection comprennant un test de
# présence à double requête (get + post)
@app.route('/newbiere', methods=['POST', 'GET'])
def newbeer():
    """Root to add a new beer, use POST to add"""
    if request.method == 'POST':
        # Recuperation of the data in the form
        # Récupération des informations depuis le formulaire
        user = request.form['newb']
        tipe = request.form['type']
        tast = request.form['tast']
        flavour = request.form['flav']
        alcool = request.form['alco']
        brasserie = request.form['brass']
        # Test of presence of the resource in the collection
        # Test de présence dans la collection
        test = Beers.find({"Nom":user, "Goût":tast, "Arômes":flavour,
                           "Alcool":alcool, "Brasserie":brasserie, "Type":tipe},
                          {"_id":0})
        json2 = dumps(test)
        if  json2 != "[]":
		          return redirect(url_for('fail_new_beer', name=user))
        else:
		          Beers.insert({"Nom":user, "Goût":tast, "Arômes":flavour,
                                "Alcool":alcool, "Brasserie":brasserie,
                                "Type":tipe})
		          return redirect(url_for('success_new_beer', name=user ))
    else:
        user = request.args.get('newb')
        tipe = request.args.get('type')
        tast = request.args.get('tast')
        flavour = request.args.get('flav')
        alcool = request.args.get('alco')
        brasserie = request.args.get('brass')
        return redirect(url_for('success_new_beer', name=user))

# Root for the success add in the collection
# Chemin route renvoyant le succes de l'ajout à la collection
@app.route('/success_new_beer/<name>')
def success_new_beer(name):
    """Root returning the sucess variable of the request"""
    return 'Nom de biere %s' % name + ' a bien ete ajoute'

# Root for the return page in case the ressource that you tryed to add is
# already existing in the Collection
# Page retour en cas de doublon dans la tentative de rentrer une nouvelle bière
@app.route('/fail_new_beer/<name>')
def fail_new_beer(name):
    """Root use to return the indication that the ressource already exist in
    the Collection
    """
    return 'Doublon, la biere : %s' %name + ' existe deja'

# Root to the html form of the add of a new beer
# Chemin route vers le formulaire html d'ajout d'une bière à la collection
@app.route('/NewBrassForm')
def NBRF():
    """Root to the html form of the add of a new brass"""
    return render_template('new_brass_form.html')

# Double request root of adding new brass to the collection whit a "already
# exist" test
# Chemin route d'ajout d'une brasserie à la collection comprennant un test de
# présence à double requête (get + post)
@app.route('/newbrass', methods=['POST', 'GET'])
def newbrass():
    """Root to add a new beer, use POST to add"""
    if request.method == 'POST':
        # Recuperation of the data in the form
        # Récupération des informations depuis le formulaire
        name = request.form['name']
        adresse = request.form['adres']
        country = request.form['count']
        beers = request.form['beers']
        past = request.form['past']
        # Collection of the geo data
    	geocode_result = gmaps.geocode(adresse)
    	for result in geocode_result:
    		try:
    			coord = result['geometry']['location']
    		except KeyError:
    			coord = None
    	lat = coord["lat"]
    	lng = coord["lng"]
    	# db.geo.insert({"adresse":geo,"loc": [lng,lat]})
        # Test of presence of the resource in the collection
        # Test de présence dans la collection
        test = Brass.find({"Nom":name, "Adresse":adresse, "Pays":country},
                          {"_id":0})
        json2 = dumps(test)
        if  json2 != "[]":
		          return redirect(url_for('fail_new_brass', name=name))
        else:
		          Brass.insert({"Nom":name, "Adresse":adresse, "Pays":country,
                          "Bières":beers, "Histoire":past, "Loc": [lng,lat]})
		          return redirect(url_for('success_new_bar', name=name))
    else:
        name = request.args.get('name')
        adresse = request.args.get('adres')
        country = request.args.get('count')
        beers = request.args.get('beers')
        past = request.args.get('past')
        return redirect(url_for('success_new_bar', name=name))

# Root for the success add of a brass to the collection
# Chemin route renvoyant le succes de l'ajout d'une brasserie à la collection
@app.route('/success_new_brass/<name>')
def success_new_brass(name):
    """Root returning the sucess of adding a brass"""
    return 'Nom de brasserie %s' % name + ' a bien ete ajoute'

# Root for the return page in case the ressource that you tryed to add is
# already existing in the Collection
# Page retour en cas de doublon dans la tentative de rentrer une nouvelle bière
@app.route('/fail_new_brass/<name>')
def fail_new_brass(name):
    """Root use to return the indication that the ressource already exist in
    the Collection
    """
    return 'Doublon, la brasserie : %s' %name + ' existe deja'

# |---------------------------------| SEARCH |---------------------------------|

# Root to the "search by name" page
# Chemin route vers page de recherche par nom
@app.route('/SearchBeerName')
def SNB():
    """Root returning the html page for the research by name"""
    return render_template('search_beer_by_name.html')

# Root to the "search by position" page
# Chemin route vers page de recherche par lieu
@app.route('/SearchBeerBrasserie')
def SAB():
    """Root returning the html page for the research by position"""
    return render_template('search_beer_by_brasserie.html')

# Root to the "search by type" page
# Chemin route vers page de recherche par type
@app.route('/SearchBeerType')
def STB():
    """Root returning the html page for the research by type"""
    return render_template('search_beer_by_type.html')

# Root to the "search brass by name" page
# Chemin route vers page de recherche brasserie par nom
@app.route('/SearchBrassByName')
def SBN():
    """Root returning the html page for the research by type"""
    return render_template('search_brass_by_name.html')

# Root to the "search bar by beer and adresse" page
# Chemin route vers page de recherche de bar par bière et adresse
@app.route('/SearchBarByBeer')
def RBBBA():
    """Root returning the html page for the research of bar by beer and adresse"""
    return render_template('geo_find.html')

# Root to a general search of resource (deliver all the data in the collection)
# Chemin route retournant toutes les ressources dans la collection
@app.route('/searchbiere', methods=['GET'])
def research():
    """Root returning a list of the json result from the search"""
    if request.method == 'GET':
        # Recuperation of the data in the form
        # Récupération des informations depuis le formulaire
        user = request.args.get('newb')
        tipe = request.args.get('type')
        tast = request.args.get('tast')
        flavour = request.args.get('flav')
        alcool = request.args.get('alco')
        brasserie = request.args.get('brass')
        data = {}
        data = Beers.find({"Nom":user, "Goût":tast, "Arômes":flavour,
                           "Alcool":alcool, "Brasserie":brasserie, "Type":tipe},
                          {"_id":0})
        return fct.returning(data)

# Root to the "search by name" algoritm
# Chemin route de recherche par nom
@app.route('/searchbierebyname', methods=['GET'])
def researchbyname():
    """Root returning a list of the json result from the search"""
    if request.method == 'GET':
        user = request.args.get('newb')
        data = {}
        data = Beers.find({"Nom":user}, {"_id":0})
        return fct.returning(data)

# Root to the "search by position" algoritm
# Chemin route de recherche par lieu
@app.route('/searchbierebybrasserie',methods=['GET'])
def researchbybrasserie():
    """Root returning a list of the json result from the search"""
    if request.method == 'GET':
        user1 = request.args.get('brass')
        data1 = {}
        data1 = Beers.find({"Brasserie":user1}, {"_id":0})
        return fct.returning(data1)

# Root to the "search by type" algoritm
# Chemin route de recherche par type
@app.route('/searchbierebytype', methods=['GET'])
def researchbytype():
    """Root returning a list of the json result from the search"""
    if request.method == 'GET':
        user2 = request.args.get('type')
        data2 = {}
        data2 = Beers.find({"Type":user2}, {"_id":0})
        return fct.returning(data2)

# Root to the "search brass" algoritm
# Chemin route de recherche de brasserie
@app.route('/searchbrasseriebyname',methods=['GET'])
def researchbrasserie():
    """Root returning a list of the json result from the search"""
    if request.method == 'GET':
	    user1 = request.args.get('brass')
	    data1 = {}
	    data1 = Brass.find({"Nom":user1}, {"_id":0})
	    return fct.returning(data1)

@app.route('/searchbarbybeer',methods=['GET'])
def researchbarbybeer():
    if request.method == 'GET':
        beers = request.args.get('beer')
        adres = request.args.get('adress')
        return fct.returning(fct.figeo2(adresse=adres, beer=beers))

@app.route('/geosuccess/<lat>,<lng>')
def success_geo(lat,lng):
    """Root returning the sucess variable of the request"""
    return (lng,lat)

# Root to the html form of the add of a new beer
# Chemin route vers le formulaire html d'ajout d'une bière à la collection
@app.route('/geofind')
def geofind():
    """Root to the html form of the add of a new beer"""
    return render_template('geo_find.html')

@app.route('/geo_find', methods=['GET'])
def findgeo():
    if request.method == 'GET':
        geo = request.args.get('geo1')
        beer1 = request.args.get('beer')
        return fct.figeo2(adresse=geo, beer=beer1)

if __name__ == '__main__':
   app.run(debug=True)
