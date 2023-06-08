#!/usr/bin/python
# coding: utf8


from datetime import datetime as dt

from marshmallow_mongoengine import ModelSchema
from marshmallow_mongoengine.fields import Nested
from . import db


class Contrat(db.Document):
    meta = {'db_alias': 'default', 'collection':'CONTRAT'}
    date_created = db.DateTimeField(default=dt.now())
    hash = db.StringField(max_length=128)
    contrat = db.StringField()

class List_contrat(db.Document):
     meta = {'db_alias': 'default', 'collection':'LIST_CONTRAT'}
     contrat = db.StringField(max_length=128)
     

class List_ville(db.Document):
     meta = {'db_alias': 'default', 'collection':'LIST_VILLE'}
     ville =  db.StringField(max_length=128)

class Region(db.Document):
    meta = {'db_alias': 'default', 'collection':'REGION'}
    date_created = db.DateTimeField(default=dt.now())
    hash = db.StringField(max_length=128)
    region = db.StringField()



class Jobs(db.Document):
    meta = {"db_alias": "default", 'collection': 'JOBS'}
    date_created = db.DateTimeField(default=dt.now())
    title = db.StringField()
    hash = db.StringField(max_length=128)
    link = db.StringField()
    competences = db.StringField()
    entreprise = db.StringField()
    date = db.StringField()
    type_job = db.StringField()
    region = db.ReferenceField(Region)
    contrat = db.ReferenceField(Contrat)

class User(db.Document):
    meta = {"db_alias": "default", 'collection': 'USER'}
    date_created = db.DateTimeField(default=dt.now())
    nom = db.StringField()
    prenoms = db.StringField()
    poste = db.StringField()
    entreprise = db.StringField()
    email = db.StringField()
    telephone = db.StringField()
    mot_passe = db.StringField()
    isFirstConnection = db.BooleanField()
    # default_mot_passe = db.StringField(null=True)
    status = db.StringField()

class Country(db.Document):
    meta = {"db_alias": "default", 'collection': 'COUNTRY'}
    nom =  db.StringField(max_length=128)
    code =  db.StringField(max_length=128)
    
class TypeChurch(db.Document):
    meta = {"db_alias": "default", 'collection': 'TYPE_CHURCH'}
    date_created = db.DateTimeField(default=dt.now())
    libelle = db.StringField()
    

class Church(db.Document):
    meta = {"db_alias": "default", 'collection': 'CHURCH'}
    date_created = db.DateTimeField(default=dt.now())
    nom = db.StringField()
    country = db.ReferenceField("Country")
    type_church = db.ReferenceField("TypeChurch")

class UserChurch(db.Document):
    meta = {"db_alias": "default", 'collection': 'USER_CHURCH'}
    date_created = db.DateTimeField(default=dt.now())
    user = db.ReferenceField("User")
    church = db.ReferenceField("Church")

    
class Member(db.Document):
    meta = {"db_alias": "default", 'collection': 'MEMBER'}
    date_created = db.DateTimeField(default=dt.now())
    nom = db.StringField()
    prenoms = db.StringField()
    email = db.StringField()
    mot_passe = db.StringField()
    role = db.ReferenceField("Role")

class Role(db.Document):
    meta = {"db_alias": "default", 'collection': 'ROLE'}
    date_created = db.DateTimeField(default=dt.now())
    libelle = db.StringField()

class ListContratSchema(ModelSchema):
    class Meta:
        model = List_contrat
class ContratSchema(ModelSchema):
    class Meta:
        model = Contrat

class ListVilleSchema(ModelSchema):
    class Meta:
        model = List_ville
class CountrySchema(ModelSchema):
    class Meta:
        model = Country
class RegionSchema(ModelSchema):
    class Meta:
        model = Region

class UserSchema(ModelSchema):
    class Meta:
        model = User

class RoleSchema(ModelSchema):
    class Meta:
        model = Role

class JobsSchema(ModelSchema):
    class Meta:
        model = Jobs
        # model_fields_kwargs = {'user_id': {'load_only': True}}
    region = Nested('RegionSchema')
    contrat = Nested('ContratSchema')

class MemberSchema(ModelSchema):
    class Meta:
        model = Member
    role = Nested('RoleSchema')

class ChurchSchema(ModelSchema):
    class Meta:
        model = Church
    country = Nested('CountrySchema')
    type_church = Nested("TypeChurchSchema")

class TypeChurchSchema(ModelSchema):
    class Meta:
        model = TypeChurch

class UserChurchSchema(ModelSchema):
    class Meta:
        model = UserChurch
    user = Nested('UserSchema')
    church = Nested('ChurchSchema')
