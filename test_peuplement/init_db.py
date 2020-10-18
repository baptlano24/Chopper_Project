# -*- coding: utf-8 -*

# Document created by :
# - Baptiste LANOUE
# - Valentin ALVES
# - Valentin VERVEUR
# Date of creation : 20/11/2018
# Date of the latest modif : 20/11/2018

# Initialisation of the test Database

# |---------------------------------| IMPORT |---------------------------------|

import json
import pymongo
import googlemaps
from flask import Flask, redirect, url_for, request, render_template, Response
from pymongo import MongoClient, GEO2D
from bson.json_util import dumps
from bson.son import SON
from datetime import datetime

# |-----------------------------| CONFIG MONGO |-------------------------------|

# Configuration of the connection whit the database
# Configuration de la connection à la database
client = MongoClient('mongodb://chopper:061094@mongodb-chopper.alwaysdata.net/chopper_beer')
app = Flask(__name__)
db = client['chopper_beer']
Beers = db.beers
Bars = db.bars
Brass = db.brass

# |--------------------------------| INDEX |-----------------------------------|

@app.route('/', methods=['GET'])
def index():
    return render_template('index_p.html')

@app.route('/test', methods=['GET'])
def test():
    datat = Bars.find({"Bieres Pressions":{"St Omer":"2,5"}})
    #datat2 = Bars.find({"Bieres Bouteilles 33":{"Guiness"}})
    jsont = dumps(datat)
    #jsont2 = dumps(datat2)
    return jsont

# |--------------------------| INIT BEER COLECTION |---------------------------|

@app.route('/initbeers', methods=['GET'])
def initbeers():
    data = [
            {
            "Nom":"St Omer",
            "Type":"Blonde",
            "Alcool":"5",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Goudale",
            "Type":"Blonde",
            "Alcool":"7,2",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Hoûblon, caramel"
            },
            {
            "Nom":"St Landelin",
            "Type":"Blonde",
            "Alcool":"5,9",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"La bière du Démon",
            "Type":"Blonde",
            "Alcool":"12",
            "Brasserie":"Gayant",
            "Goût":"Fort en alcool",
            "Arômes":"Alcool et blé"
            },
            {
            "Nom":"Bière du désert",
            "Type":"Blonde",
            "Alcool":"7,2",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Amadeus",
            "Type":"Blanche",
            "Alcool":"4,5",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Tequeros",
            "Type":"Aromatisé",
            "Alcool":"5,6",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"La Démon",
            "Type":"Blonde",
            "Alcool":"8,5",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Goldenberg",
            "Type":"Blonde",
            "Alcool":"5,9",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Brune artisanale",
            "Type":"Brune",
            "Alcool":"6,4",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Celta",
            "Type":"Blonde",
            "Alcool":"SA",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Saaz",
            "Type":"Blonde",
            "Alcool":"5,2",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"La Raoul",
            "Type":"Blonde",
            "Alcool":"7,2",
            "Brasserie":"Gayant",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"La Chouffe",
            "Type":"Blonde",
            "Alcool":"8",
            "Brasserie":"Achouffe",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Mc Chouffe",
            "Type":"Brune",
            "Alcool":"8",
            "Brasserie":"Achouffe",
            "Goût":"Classique",
            "Arômes":"Hoûblon, caramel"
            },
            {
            "Nom":"Houblon Chouffe",
            "Type":"Blonde",
            "Alcool":"9",
            "Brasserie":"Achouffe",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"N'Ice Chouffe",
            "Type":"Ambrée",
            "Alcool":"10",
            "Brasserie":"Achouffe",
            "Goût":"Fort en alcool",
            "Arômes":"Alcool et blé"
            },
            {
            "Nom":"Chouffe Soleil",
            "Type":"Aromatisé",
            "Alcool":"6",
            "Brasserie":"Achouffe",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Chouffe Bok",
            "Type":"Ambrée",
            "Alcool":"6,66",
            "Brasserie":"Achouffe",
            "Goût":"Classique",
            "Arômes":"Classique"
            },
            {
            "Nom":"Cherry Chouffe",
            "Type":"Aromatisé",
            "Alcool":"8",
            "Brasserie":"Achouffe",
            "Goût":"Kriek",
            "Arômes":"Cerise"
            }
            ]

    Beers.insert(data)
    return "all append fine"

# |------------------------| INIT BRASS COLECTION |----------------------------|

@app.route('/initbrass', methods=['GET'])
def initbrass():
    data = [
            {
            "Nom":"Gayant",
            "Adresse":"Avenue Newton, 62510 Arques",
            "Pays":"France",
            "Bieres":["Goudale", "Saint Landelin", "La bière du Démon",
                      "Bière du désert", "Amadeus", "Tequieros", "La Démon",
                      "Goldenberg", "Brune artisanale", "Celta", "Saaz",
                      "La Raoul"],
            "Histoire":"En 1919 à Douai, quatre brasseries se réunissent pour former La grande brasserie des enfants de Gayant. La bière sans alcool Celta est lancée en 1970, la Goudale en 1994. Le changement de nom intervient en 1995. En 2001, la brasserie de Gayant prend le contrôle de la Brasserie Vandamme, située à Ronchin, qui fabrique les bières Triple Secret des Moines, Grain d'Orge, Ambrée des Flandres, Septante 5 et Belzébuth. Renommée l'année suivante en Brasserie Grain d'Orge, celle-ci est fermée en 2005, et la fabrication est transférée à Douai. En 2010, la famille d'Aubreby, qui possédait la brasserie depuis 1955, la revend à André Pecqueur, qui possède la Brasserie de Saint-Omer. Le site de production s'installe à Arques en 2017 afin de se rapprocher de celui de la Brasserie de Saint-Omer, elle prend le nom de Brasserie Goudale. ",
            "Loc":[2.32242210000004,50.73202860000001],
            "Distance":"0"
            },
            {
            "Nom":"Achouffe",
            "Adresse":"Achouffe",
            "Pays":"Belgique",
            "Bieres":["La Chouffe", "Mc Chouffe", "Houblon Chouffe",
                      "N'Ice Chouffe", "Chouffe Soleil", "Chouffe Bok",
                      "Cherry Chouffe"],
            "Histoire":" Située au cœur de la verdoyante Ardenne belge, notre Brasserie est spécialisée dans le brassage de bières spéciales de qualité. Notre histoire commence à la fin des années septante, lorsque deux beaux-frères, Pierre Gobron et Chris Bauweraerts, décident de créer leur propre bière et ce, dans leur propre brasserie. Avec le peu d'argent dont ils disposent à l’époque (200.000BEF, moins de 5.000€), ils entament ce que les fans de la brasserie appellent une « Chouffe story ». Au départ considérée comme un hobby, la Brasserie d'Achouffe connaît un développement tel que Pierre et Chris décident de se lancer l'un après l'autre à plein temps dans l'aventure. Le premier brassin de LA CHOUFFE (49 litres) est produit le 27 août 1982. Les lutins d'Achouffe veulent très vite découvrir d'autres contrées, et leurs cousins néerlandais sont les premiers à leur réserver un accueil chaleureux. De nos jours, plus de 40 pays de par le monde sont approvisionnés en bière d’Achouffe. Des récompenses internationales très convoitées sont aussi venues, année après année, couronner leur saveur unique. A la fin de l'été 2006, les fondateurs de la Brasserie choisissent de confier la destinée de leurs chers lutins à la Brasserie Duvel-Moortgat. La volonté du groupe est d'investir à Achouffe et de développer le potentiel de la Brasserie. Depuis lors, de nombreux travaux ont été entrepris pour embellir la brasserie et ses alentours, et nos Bières ont pu trouver de nouvelles destinations aux quatre coins du globe. Une fierté pour tous les lutins et l’équipe d’Achouffe !",
            "Loc":[5.740859999999998,50.14958],
            "Distance":"0"
            }
            ]

    Brass.create_index([("Loc", GEO2D)])
    Brass.insert(data)
    return "all append fine"

# |--------------------------| INIT BAR COLECTION |----------------------------|

@app.route('/initbars', methods=['GET'])
def initbars():
    data = [
            {
            "Nom":"Le Nautilus",
            "Adresse":"12 Place des jacobins, 29600 Morlaix",
            "Pays":"France",
            "Horaires":{"Lundi":"0", "Mardi":"18h00-01h00",
                         "Mercredi":"18h00-01h00", "Jeudi":"18h00-01h00",
                         "Vendredi":"18h00-01h00", "Samedi":"18h00-01h00",
                         "Dimanche":"18h00-01h00"},
            "Bieres":["St Omer","Goudale","Ciney"],
            "Bieres Pressions":[{"Nom":"St Omer","Prix":"2.5"}, {"Nom":"Goudale","Prix":"3.4"}, {"Nom":"Ciney","Prix":"4"}],
            "Bieres Bouteilles":[{"Nom":"Guiness","Prix":"4"}, {"Nom":"Kilkenny","Prix":"4"}],
            "Loc":[-3.825701699999968,48.57708839999999],
            "Distance":"0"
            },
            {
            "Nom":"La Cave",
            "Adresse":"6 Avenue du Ponceau, 95000 Cergy",
            "Pays":"France",
            "Horaires":{"Lundi":"20h00-01h30", "Mardi":"20h00-01h30",
                         "Mercredi":"20h00-01h30", "Jeudi":"20h00-01h30",
                         "Vendredi":"20h00-01h30", "Samedi":"0",
                         "Dimanche":"0"},
            "Bieres":["Felsgold","La Chouffe","Triple Karmeliet","Goudale","Cuvée des Trolls"],
            "Bieres Pressions":[{"Nom":"Felsgold","Prix":"1.5"}, {"Nom":"La Chouffe","Prix":"2"}],
            "Bieres Bouteilles":[{"Nom":"Triple Karmeliet","Prix":"3"}, {"Nom":"Goudale","Prix":"2.5"}, {"Nom":"Cuvée des Trolls","Prix":"2.5"}],
            "Loc":[2.072387899999967,49.0393601],
            "Distance":"0"
            },
            {
            "Nom":"Le Reve",
            "Adresse":"14 allée de l'Isara, 95000 Cergy",
            "Pays":"France",
            "Horaires":{"Lundi":"20h00-01h30", "Mardi":"20h00-01h30",
                         "Mercredi":"20h00-01h30", "Jeudi":"20h00-01h30",
                         "Vendredi":"20h00-01h30", "Samedi":"0",
                         "Dimanche":"0"},
            "Bieres":["Felsgold","Triple Karmeliet","Goudale","Cuvée des Trolls"],
            "Bieres Pressions":[{"Nom":"Felsgold","Prix":"1.5"}, {"Nom":"La Chouffe","Prix":"2"}],
            "Bieres Bouteilles":[{"Nom":"Triple Karmeliet","Prix":"3"}, {"Nom":"Goudale","Prix":"2.5"}, {"Nom":"Cuvée des Trolls","Prix":"2.5"}],
            "Loc":[2.067093,49.03270089999999],
            "Distance":"0"
            },
            {
            "Nom":"La kolloc",
            "Adresse":"10 rue de marseille, Lyon",
            "Pays":"France",
            "Horaires":{"Lundi":"20h00-01h30", "Mardi":"20h00-01h30",
                         "Mercredi":"20h00-01h30", "Jeudi":"20h00-01h30",
                         "Vendredi":"20h00-01h30", "Samedi":"0",
                         "Dimanche":"0"},
            "Bieres":["Felsgold","Triple Karmeliet","Goudale","Cuvée des Trolls"],
            "Bieres Pressions":[{"Nom":"Felsgold","Prix":"1.5"}, {"Nom":"La Chouffe","Prix":"2"}],
            "Bieres Bouteilles":[{"Nom":"Triple Karmeliet","Prix":"3"}, {"Nom":"Goudale","Prix":"2.5"}, {"Nom":"Cuvée des Trolls","Prix":"2.5"}],
            "Loc":[4.8395585,45.752293],
            "Distance":"0"
            }
            ]

    db.bars.create_index([("Loc", GEO2D)])
    Bars.insert(data)
    return "all append fine"

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

if __name__ == '__main__':
   app.run(debug=True)
