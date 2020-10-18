# -*- coding: utf-8 -*

# Document cself.03333333333330re00000003ated by :
# - Baptiste LANOUE
# - Valentin ALVES
# - Valentin VERVEUR
# Date of creation : 20/11/2018
# Date of the latest modif : 30/01/2019


                              ##############
#-----------------------------### IMPORT ###------------------------------------
                              ##############

import json
import pymongo
import math
from flask import Flask, redirect, url_for, request, render_template, Response, make_response, jsonify, send_file
from pymongo import MongoClient, GEO2D
from bson.json_util import dumps
from flask_cors import CORS

from db import connect
from functions import fct




                          ####################
#-------------------------### CONFIG MONGO ###----------------------------------
                          ####################



# Configuration of the connection whit the database
# Configuration de la connection à la database
app = Flask(__name__)
CORS(app)
Beers = connect.db.beers
Brass = connect.db.brass
Bars = connect.db.bars
namemodif = None


#modif pour commit

                         #######################
#------------------------### KILL COLLECTION ###--------------------------------
                         #######################



# ---------------------------------Kill beer------------------------------------


@app.route('/killbeers', methods=['GET', 'PUT'])
def kill_beers():
    Beers.drop()
    return "Collection droped"


# ---------------------------------Kill brass-----------------------------------


@app.route('/killbrass', methods=['GET', 'PUT'])
def kill_brass():
    Brass.drop()
    return "Collection droped"


# ---------------------------------Kill bars------------------------------------


@app.route('/killbars', methods=['GET', 'PUT'])
def kill_bars():
    Bars.drop()
    return "Collection droped"




                         ##########################
#------------------------### DELETE A RESSOURCE ###-----------------------------
                         ##########################




# -------------------------------Delete a beer----------------------------------


@app.route('/DeleteBeer')
def DAB():
    """Root to the html form of the add of a new beer"""
    return render_template('delete_beer_by_name.html')



# A therme, la methods doit être delete
@app.route('/dropabeer', methods=['POST'])
def drop_a_beer():
    name = request.form['beer']
    Beers.delete_one({"Nom":name})
    data = Beers.find({"Nom":name} , {"_id":0})
    return fct.returning(data)



# -------------------------------Delete a brass---------------------------------



@app.route('/DeleteBrass')
def DABR():
    """Root to the html form of the add of a new beer"""
    return render_template('delete_brass_by_name.html')



# A therme, la methods doit être delete
@app.route('/dropabrass', methods=['POST'])
def drop_a_brass():
    name = request.form['brass']
    Brass.delete_one({"Nom":name})
    data = Brass.find({"Nom":name} , {"_id":0})
    return fct.returning(data)



# -------------------------------Delete a bar-----------------------------------


@app.route('/DeleteBar')
def DABA():
    """Root to the html form of the add of a new beer"""
    return render_template('delete_bar_by_name.html')



# A therme, la methods doit être delete
@app.route('/dropabar', methods=['POST'])
def drop_a_bar():
    name = request.form['bar']
    Bars.delete_one({"Nom":name})
    data = Bars.find({"Nom":name} , {"_id":0})
    return fct.returning(data)



                                 #############
#--------------------------------### INDEX ###----------------------------------
                                 #############




# Root for the index page
# Chemin route vers la page d'index
@app.route('/', methods=['GET'])
def home():
    """Root for the index page"""
    return render_template('index.html')




                           #######################
#--------------------------### ADD A RESSOURCE ###------------------------------
                           #######################



# ----------------------------------New beer------------------------------------


# Root to the html form of the add of a new beer
# Chemin route vers le formulaire html d'ajout d'une bière à la collection
@app.route('/NewBeerForm')
def NBF():
    """Root to the html form of the add of a new beer"""
    return render_template('new_beer_form.html')



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
        test = fct.test_presence(user , Beers)
        if test == False :
            Beers.insert({"Nom":user, "Goût":tast, "Arômes":flavour, "Alcool":alcool, "Brasserie":brasserie, "Type":tipe})
            return "sucess"
        else :
            return "fail"



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



# ----------------------------------New bar-------------------------------------


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
        lat = 0
        lng = 0
        if adresse != "" :
            coord = fct.find_loc(adresse)
        else :
            coord = [0,0]
        schedule = {"Lundi":schedule1 , "Mardi":schedule2 , "Mercredi":schedule3 , "Jeudi":schedule4 , "Vendredi":schedule5 , "Samedi":schedule6 , "Dimanche":schedule7}

        # Test of presence of the resource in the collection
        # Test de présence dans la collection
        test = fct.test_presence(name , Bars)
        if test == True :
            return redirect(url_for('fail_new_bar', name=name))
        else:
			
            Bars.insert({"Nom":name, "Adresse":adresse, "Pays":country, "Horaires":schedule, "Bières":beers, "Bieres Pressions":pbeers, "Bieres Bouteilles":botbeers, "Loc": [coord[1],coord[0]]})
 
            return redirect(url_for('success_new_bar', name=name))



# Root for the success add of a bar to the collection
# Chemin route renvoyant le succes de l'ajout d'un bar à la collection
@app.route('/success_new_bar/<name>')
def success_new_bar(name):
    """Root returning the sucess of adding a bar"""
    return 'Nom ddu bar %s' % name + ' a bien ete ajoute'



@app.route('/fail_new_bar/<name>')
def fail_new_bar(name):
    """Root use to return the indication that the ressource already exist in
    the Collection
    """
    return 'Doublon, le bar : %s' %name + ' existe deja'



# ----------------------------------New brass-----------------------------------


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
        if adresse != "" :
            coord = fct.find_loc(adresse)
        else :
            coord = [0,0]
        # db.geo.insert({"adresse":geo,"loc": [lng,lat]})
        # Test of presence of the resource in the collection
        # Test de présence dans la collection
        test = fct.test_presence(name , Brass)
        if test == False :
            return redirect(url_for('fail_new_brass', name=name))
        else:
            Brass.insert({"Nom":name, "Adresse":adresse, "Pays":country, "Bières":beers, "Histoire":past, "Loc": [coord[1],coord[0]]})
            return redirect(url_for('success_new_bar', name=name))



# Root for the success add of a brass to the collection
# Chemin route renvoyant le succes de l'ajout d'une brasserie à la collection
@app.route('/success_new_brass/<name>')
def success_new_brass(name):
    """Root returning the sucess of adding a brass"""
    return 'Nom de brasserie %s' % name + ' a bien ete ajoute'



# Root for the return page in case the ressource that you tryed to add is
# already existing in the Collection
# Page retur en cas de doublon dans la tentative de rentrer une nouvelle bière
@app.route('/fail_new_brass/<name>')
def fail_new_brass(name):
    """Root use to return the indication that the ressource already exist in
    the Collection
    """
    return 'Doublon, la brasserie : %s' %name + ' existe deja'





                      #################################
#---------------------### MODIFICATION OF RESSOURCE ###-------------------------
                      #################################





                              ##############
#-----------------------------### SEARCH ###------------------------------------
                              ##############



# -----------------------------Search beer by name------------------------------


# Root to the "search by name" page
# Chemin route vers page de recherche par nom
@app.route('/SearchBeerName')
def SNB():
    """Root returning the html page for the research by name"""
    return render_template('search_beer_by_name.html')



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
        data = Beers.find({"Nom":user, "Goût":tast, "Arômes":flavour, "Alcool":alcool, "Brasserie":brasserie, "Type":tipe}, {"_id":0})
        return fct.returning(data)



# -----------------------------Search beer by brass-----------------------------


# Root to the "search by position" page
# Chemin route vers page de recherche par lieu
@app.route('/SearchBeerBrasserie')
def SAB():
    """Root returning the html page for the research by position"""
    return render_template('search_beer_by_brasserie.html')



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




# -----------------------------Search beer by type------------------------------


# Root to the "search by type" page
# Chemin route vers page de recherche par type
@app.route('/SearchBeerType')
def STB():
    """Root returning the html page for the research by type"""
    return render_template('search_beer_by_type.html')



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




# -----------------------------Search brass by name-----------------------------


# Root to the "search brass by name" page
# Chemin route vers page de recherche brasserie par nom
@app.route('/SearchBrassByName')
def SBN():
    """Root returning the html page for the research by type"""
    return render_template('search_brass_by_name.html')



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




# -------------------------Search bar by beer and loc---------------------------


# Root to the "search bar by beer and adresse" page
# Chemin route vers page de recherche de bar par bière et adresse
@app.route('/SearchBarByBeer')
def RBBBA():
    """Root returning the html page for the research of bar by beer and adresse"""
    return send_file('Jquery.html')



@app.route('/searchbarbybeer',methods=['GET'])
def researchbarbybeer():
    if request.method == 'GET':
        beers = request.args.get('nom')
        lon = request.args.get('lon')
        lat = request.args.get('lat')

        return fct.figeo2(lon=lon, lat=lat, beer=beers)





if __name__ == '__main__':
    app.run(debug=True)
