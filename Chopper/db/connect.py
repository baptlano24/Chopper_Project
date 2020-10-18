import pymongo
from flask import Flask, redirect, url_for, request, render_template, Response, make_response, jsonify
from pymongo import MongoClient, GEO2D

client = MongoClient('mongodb://chopper:061094@mongodb-chopper.alwaysdata.net/chopper_beer')
db = client['chopper_beer']
