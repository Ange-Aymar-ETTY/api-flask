

from flask_restful import Resource
import requests
from flask import Response,request
from ..models import Jobs,Region,RegionSchema,Contrat,ContratSchema,JobsSchema,List_ville,List_contrat,ListContratSchema,ListVilleSchema,User,UserSchema,Role,RoleSchema,Member,MemberSchema,UserChurch,UserChurchSchema,Church,ChurchSchema,CountrySchema,Country,TypeChurch,TypeChurchSchema
from ..utilities import senMail,success,error,generateString,create_jwt_token,decode_jwt_token,verifEmailAdress
from flask_jwt_extended import create_access_token,jwt_required
import logging
import hashlib
from datetime import datetime, timedelta
import time
from .mailTemplate import confirmMailTemplate,forgotPasswordTemplate
from mongoengine.queryset.visitor import Q

class IndexResource(Resource):
    def get(self):
        return "Application is running"

class FindAllCities(Resource):
    def get(self, filters=None):
        try:
            villes = List_ville.objects()
            output = ListVilleSchema(many=True).dump(villes)
            total = villes.count()
            return success("Succès",  {'ville':output, 'total':total}, 200)
        except Exception as ex:
            logging.error(ex)
            return error(ex, 200)

class FindAllCountries(Resource):
     def get(self, filters=None):
        try:
            country = Country.objects()
            output = CountrySchema(many=True).dump(country)
            total = country.count()
            print(output)
            return success("Succès",  {'country':output, 'total':total}, 200)
        except Exception as ex:
            logging.error(ex)
            return error(ex, 200)

class FindAllContrat(Resource):
    def get(self, filters=None):
        try:
            contrat = List_contrat.objects()
            total = contrat.count()
            output = ListContratSchema(many=True).dump(contrat)
            return success("Succès",  {'contrat':output, 'total':total}, 200)
        except Exception as ex:
            logging.error(ex)
            return error(ex, 200)


class FindAllChurch(Resource):
    def get(self, filters=None):
        try:
            church = Church.objects()
            print("output",church)
            output = ChurchSchema(many=True).dump(church)
            print("output",output)
            total = church.count()
            return success("Succès", {'church':output, 'total':total}, 200)#{'church':output, 'total':total}
        except Exception as ex:
            logging.error(ex)
            return error(ex, 200)

class FindAllUsers(Resource):
    def get(self, filters=None):
        
        try: 
            user = User.objects()
            regions = Region.objects()
            total = user.count()
            if filters is None:
                print('iiv')
                #output = jsonify(result)
                output = UserSchema(many=True).dump(user)
                for i in output:
                    if i.get("mot_passe"):
                        del i["mot_passe"]
                print('output',output)
            else:
                filtres = filters.split('&')
                page = 1
                nbre = 25
                filters = {}
                for f in filtres:
                    elt = f.split('=')
                    if len(elt) == 2:
                        filters[elt[0]] = int(elt[1])
                if filters.get('page'):
                    page = filters['page']
                    
                if filters.get('nbre'):
                    nbre = filters['nbre']
                print(User.objects())
                output = User.objects()[(nbre*(page-1)):(nbre*page)]
                output = UserSchema(many=True).dump(output)
                for i in output:
                    if i.get("mot_passe"):
                        del i["mot_passe"]
            return success("Succès",  {'user':output, 'total':total}, 200)
        except Exception as ex:
            logging.error(ex)
            return error(ex, 200)

class UserDetails(Resource):
    def get(self, filters=None):
        try:
            if filters is not None:
                user = User.objects(id=filters)
                print("output",user)
                output = UserSchema(many=True).dump(user)
                print("output",output)
                total = user.count()
                for i in output:
                    if i.get("mot_passe"):
                        del i["mot_passe"]
                return success("Succès", {'user':output, 'total':total}, 200)#{'church':output, 'total':total}
            else:
                return error("Aucune information sur cet utilisateur", status)
        except Exception as ex:
            logging.error(ex)
            return error(ex, 200)

class FindAllTypeChurch(Resource):
    def get(self, filters=None):
        try:
            type_church = TypeChurch.objects()
            output = TypeChurchSchema(many=True).dump(type_church)
            total = type_church.count()
            return success("Succès",  {'church':output, 'total':total}, 200)
        except Exception as ex:
            logging.error(ex)
            return error(ex, 200)
class FindAllOffer(Resource):
    def get(self, filters=None):
        
        try: 
            jobs = Jobs.objects()
            regions = Region.objects()
            total = jobs.count()
            if filters is None:
                print('iiv')
                #output = jsonify(result)
                output = JobsSchema(many=True).dump(jobs)
                print('output',output)
            else:
                filtres = filters.split('&')
                page = 1
                nbre = 25
                filters = {}
                for f in filtres:
                    elt = f.split('=')
                    if len(elt) == 2:
                        filters[elt[0]] = int(elt[1])
                if filters.get('page'):
                    page = filters['page']
                    
                if filters.get('nbre'):
                    nbre = filters['nbre']
                print(Jobs.objects())
                output = Jobs.objects()[(nbre*(page-1)):(nbre*page)]
                output = JobsSchema(many=True).dump(output)
            return success("Succès",  {'jobs':output, 'total':total}, 200)
        except Exception as ex:
            logging.error(ex)
            return error(ex, 200)

class FindOffersByContrat(Resource):
    def get(self,filters=None):
        filtres = filters.split('&')
        print("split",filtres)
        print("splo",filtres[0].split(","))
        filter_region= filtres[0].split(",")
        page = 1
        nbre = 25
        filters = {}
        total = 0
        for f in filtres:
            
            elt = f.split('=')
            print(elt)
            if len(elt) == 2:
                filters[elt[0]] = int(elt[1])
            if filters.get('page'):
                page = filters['page']     
            if filters.get('nbre'):
                nbre = filters['nbre']
        if filters is not None:
            if len(filtres) >= 2: 
                jobs = Jobs.objects()[(nbre*(page-1)):(nbre*page)]
            else:
                jobs = Jobs.objects()
            if jobs is not None:
                job= [x for x in jobs]
                liste  = []
                for i in job:
                    for j in filter_region:
                        if j.upper() in i['contrat']['contrat']:
                            liste.append(i)
                contrat = JobsSchema(many=True).dump(liste)
            else:
                contrat = []

        else:
            contrat = []
        return success("Succès", {'jobs':contrat, 'total':len(contrat)}, 200)

class FindOffersByRegion(Resource):
    def get(self,filters=None):
        filtres = filters.split('&')
        print("split",filtres)
        print("splo",filtres[0].split(","))
        filter_region= filtres[0].split(",")
        page = 1
        nbre = 25
        filters = {}
        for f in filtres:
            
            elt = f.split('=')
            print(elt)
            if len(elt) == 2:
                filters[elt[0]] = int(elt[1])
            if filters.get('page'):
                page = filters['page']     
            if filters.get('nbre'):
                nbre = filters['nbre']
        if filters is not None:
            if len(filtres) >= 2: 
                jobs = Jobs.objects()[(nbre*(page-1)):(nbre*page)]
            else:
                jobs = Jobs.objects()
            if jobs is not None:
                job= [x for x in jobs]
                liste  = []
                for i in job:
                    for j in filter_region:
                        if j.upper() in i['region']['region']:
                            liste.append(i)
                regions = JobsSchema(many=True).dump(liste)
            else:
                regions = []

        else:
            regions = []
        return success("Succès", {'jobs':regions, 'total':len(regions)}, 200)
    

class FindOffersByContratRegion(Resource):
    def get(self,filters=None):
        filtres = filters.split('&')
        print("split",filtres)
        
        if len(filters) == 0:
            return success("Succès", {'jobs': [], 'total':0}, 200)
        
        print("splo",filtres[0].split(","))
        filter_params = filtres[0].split(",")
        if len(filter_params) == 0:
            return success("Succès", {'jobs': [], 'total':0}, 200)
        else:
            print(f'longeur elts => {len(filter_params)}')
            page = 1
            nbre = 25
            filters = {}
            for f in filtres:
                elt = f.split('=')
                print(elt)
                if len(elt) == 2:
                    filters[elt[0]] = int(elt[1])
                if filters.get('page'):
                    page = filters['page']     
                if filters.get('nbre'):
                    nbre = filters['nbre']
                    
            ##### Check contract type or region
            contrat = []
            region = []
            filter_params = [x.upper() for x in filter_params]
            contrats = []
            for x in filter_params:
                contrat = Contrat.objects(contrat__contains=x)
                if contrat is not None:
                    for c in contrat:
                        contrats.append(c)
                    filter_params.remove(x)
            
            regions = []
            for x in filter_params:
                region = Region.objects(region__contains=x)
                if region is not None:
                    for r in region:
                        regions.append(r)
                    filter_params.remove(x)

            if contrats is not None:
                if regions is not None:
                    jobs = Jobs.objects(Q(region__in=region) & Q(contrat__in=contrats))[(nbre*(page-1)):(nbre*page)]
                    total = Jobs.objects(Q(region__in=region) & Q(contrat__in=contrats)).count()
                else:
                    jobs = Jobs.objects(contrat__in=contrats)[(nbre*(page-1)):(nbre*page)]
                    total = Jobs.objects(contrat__in=contrats).count()
            else:
                if regions is not None:
                    region = [x for x in regions]
                    jobs = Jobs.objects(region__in=region)[(nbre*(page-1)):(nbre*page)]
                    total = Jobs.objects(region__in=region).count()
                else:
                    jobs = None
                    total = 0
            
            if jobs is not None:
                contrats = JobsSchema(many=True).dump(jobs)
            else:
                contrats = []
        
        return success("Succès", {'jobs':contrats, 'total':total}, 200)
    
class InscriptionUser(Resource):
    def post(self):
        try:
            body = request.get_json()
            body_user = {
                "nom":body["nom"],
                "prenoms":body["prenoms"],
                "poste":body["poste"],
                "mot_passe":hashlib.md5("Password2023".encode('utf-8')).hexdigest(),
                # "default_mot_passe":hashlib.md5("Password2023".encode('utf-8')).hexdigest(),
                "entreprise":body["entreprise"],
                "email":body["email"],
                "isFirstConnection":True,
                "telephone":body["telephone"],
            }
            if(verifEmailAdress(body["email"]) == False):
                return error("Entrer une adresse mail valide", 500)
            print("body",body_user)
            body["statut"] = 0
            # body["default_mot_passe"] = "Password2023"
            user_exist_telephone = User.objects(telephone=body["telephone"])
            print("user_exist_telephone",user_exist_telephone)
            user_exist_email = User.objects(email=body["email"])
            print("user_exist_email",user_exist_email)
            if len(user_exist_telephone) > 0 :
                return error("Ce numero de telephone existe déjà dans la base", 500) 
            elif len(user_exist_email) > 0:
                 return error("Cette adresse email existe déjà dans la base", 500)
            else:
                type_church = TypeChurch.objects(id=body["type_church"])
                type_church = TypeChurchSchema().dump(type_church[0])
                print('libelle',type_church)
                result_church = {}
                if(type_church["libelle"] == "OTHER"):
                    print('result',result_church)
                    body_church = {
                        "type_church":body["type_church"],
                        "nom":body["nom_church"],
                        "country":body["country"]
                    }
                    result_church = Church(**body_church).save()
                    print('result',result_church)
                    result_church = ChurchSchema().dump(result_church)
                    body["church"] = result_church["id"]
                    body["default_mot_passe"] = hashlib.md5("Password2023".encode('utf-8')).hexdigest()
                    user = User(**body_user).save()
                    result_user = UserSchema().dump(user)
                    userchurch = {"user":result_user["id"],"church":body["church"]}
                    uc = UserChurch(**userchurch).save()
                    print(uc)
                else:
                    print('result 2',result_church)
                    body["default_mot_passe"] = hashlib.md5("Password2023".encode('utf-8')).hexdigest()
                    user = User(**body_user).save()
                    result_user = UserSchema().dump(user)
                    userchurch = {"user":result_user["id"],"church":body["church"]}
                    uc = UserChurch(**userchurch).save()
                    print(uc)
                x = senMail(confirmMailTemplate(body["prenoms"], body["email"], "Password2023"), body["email"])
                print("request",x)
                return success("Succès", {'data':UserSchema().dump(user)}, 200)  
        except Exception as ex:
            return error("Une erreur est survenue: " + str(ex), 500)

class LoginUser(Resource):
    def post(self):
        try:
            body = request.get_json()
            body["mot_passe"] = hashlib.md5(body["mot_passe"].encode('utf-8')).hexdigest()
            user_email = User.objects(email=body["email"])
            print("user_email",UserSchema().dump(user_email[0]))
            if len(user_email) > 0:
                user = UserSchema().dump(user_email[0])  
                print("user",user)
                if user["mot_passe"] == body["mot_passe"]:
                    if user.get('mot_passe'):
                        del user['mot_passe']
                    return success("Connexion réussie", user, 200)
                else:
                    return error("Email ou mot de passe incorrect", 200)
            else:
                return error("Email ou mot de passe incorrect", 200)
        except Exception as ex:
            return error("Une erreur est survenue: " + str(ex), 500)
        

class resetUserPassword(Resource):
    def put(self,filters=None):
        try:
            print("?????")
            body = request.get_json()
            if(body["mot_passe"] == "Password2023"):
                return error("Veuillez entrer un autre mot de passe", 500)
            elif filters is None:
                return error("L'utilsateur n'existe pas", 500)
            else:
                body["mot_passe"] = hashlib.md5(body["mot_passe"].encode('utf-8')).hexdigest()
                body["default_mot_passe"] = ""
                user = User.objects.get(id=filters).update(**body)
                return success("Succès", UserSchema().dump(user), 200)
        except Exception as ex:
            return error("Une erreur est survenue: " + str(ex), 500) 


class sendUserMail(Resource):
  def post(self):
    try:
        body = request.get_json()
        global code
        global token
        code = generateString(5)
        user_email = User.objects(email=body["email"])
        token = create_jwt_token(UserSchema().dump(user_email[0]) )
        print("token",token)
        print("user_email",user_email[0]["mot_passe"])
        if len(user_email) > 0:
            x = senMail(forgotPasswordTemplate(user_email[0]["prenoms"], code), body["email"])
            print("request",x)
            return success("Succès",UserSchema().dump(user_email[0])["id"], 200)
        else:
            return error("L'utilsateur n'existe pas", 500)
    except Exception as ex:
        return error("Une erreur est survenue: " + str(ex), 500)    
    

class changeUserPassword(Resource):
    def put(self,filters=None):
        try:
            global code
            global token
            body = request.get_json()
            user = User.objects(id=filters)
            if(body["mot_passe"] == "Password2023"):
                return error("Veuillez entrer un autre mot de passe", 500)
            elif(hashlib.md5(body["mot_passe"].encode('utf-8')).hexdigest() == user[0]["mot_passe"]):
                return error("Veuillez entrer un autre mot de passe", 500)
            elif filters is None:
                return error("L'utilsateur n'existe pas", 500)
            else:
                print("code",code)
                token = decode_jwt_token(token)
                exp = token.get("exp")
                print("token",exp)
                if(exp > time.time()):
                    if(code == body["code"].strip()):
                        body["mot_passe"] = hashlib.md5(body["mot_passe"].encode('utf-8')).hexdigest()
                        body_update = {"mot_passe":body["mot_passe"],"isFirstConnection":False}
                        user_update = User.objects.get(id=filters).update(**body_update)
                        return success("Succès", UserSchema().dump(user_update), 200)
                    else:
                        return error("Le code n'est pas valide", 500)
                else:
                    return error("Le token a expiré", 500)
        except Exception as ex:
            return error("Une erreur est survenue: " + str(ex), 500)

class LoginMember(Resource):
    def post(self):
        try:
            body = request.get_json()
            body["mot_passe"] = hashlib.md5(body["mot_passe"].encode('utf-8')).hexdigest()
            user_email = Member.objects(email=body["email"])
            # print("user_email",user_email[0]["mot_passe"])
            if len(user_email) > 0:
                member = MemberSchema().dump(user_email[0])
                if member["mot_passe"] == body["mot_passe"]:
                    expires = timedelta(minutes=30)
                    access_token = create_access_token(identity=str(member["id"]),expires_delta=expires)
                    member["token"] = access_token
                    return success("Connexion réussie", member.exclude('mot_passe'), 200)
                else:
                    return error("Email ou mot de passe incorrect", 200)
            else:
                    return error("Email ou mot de passe incorrect", 200)
        except Exception as ex:
            return error("Une erreur est survenue: " + str(ex), 500)

class createMember(Resource):
     @jwt_required()
     def post(self,filters=None):
        try:
            body = request.get_json()
            print("body",body)
            member_role = Role.objects(id=body["member_role"])
            member_role = RoleSchema().dump(member_role[0])
            print("member_role",member_role)
            user_exist_email = Member.objects(email=body["email"])
            print("user_exist_email",user_exist_email)
            if len(user_exist_email) > 0:
                 return error("Cette adresse email existe déjà dans la base", 500)
            else:
                if(member_role["libelle"] == "Admin"): 
                    body["mot_passe"] = hashlib.md5("Password2023".encode('utf-8')).hexdigest()
                    body_update = {"nom":body["nom"],
                                "prenoms":body["prenoms"],
                                "email":body["email"],
                                "mot_passe":hashlib.md5("Password2023".encode('utf-8')).hexdigest(),
                                "role":body["role"]
                                }
                    print("body_update",body_update)
                    x = senMail(confirmMailTemplate(body["prenoms"], body["email"], "Password2023"), body["email"])
                    member = Member(**body_update).save()
                    return success("Succès", MemberSchema().dump(member).pop('mot_passe',None), 200) 
                else:
                     return error("Vous devez être administrateur pour enregister un membre.", 500)
        except Exception as ex:
            return error("Une erreur est survenue: " + str(ex), 500)

class resetPassword(Resource):
    def put(self,filters=None):
        try:
            body = request.get_json()
            if(body["mot_passe"] == "Password2023"):
                return error("Veuillez entrer un autre mot de passe", 500)
            elif filters is None:
                return error("L'utilsateur n'existe pas", 500)
            else:
                body["mot_passe"] = hashlib.md5(body["mot_passe"].encode('utf-8')).hexdigest()
                member = Member.objects.get(id=filters).update(**body)
                return success("Succès", MemberSchema().dump(member), 200)
        except Exception as ex:
            return error("Une erreur est survenue: " + str(ex), 500) 

class listUsers(Resource):
    @jwt_required()
    def get(self,filters=None):
            try:
                if filters is None:
                    users = User.objects()
                    output = UserSchema(many=True).dump(users.exclude('mot_passe'))
                    return success("Succès", output, 200)
                else:
                    users = User.objects(id=filters)
                    output = UserSchema().dump(users.exclude('mot_passe'))
                    return success("Succès", output, 200)
            except Exception as ex:
                return error("Une erreur est survenue: " + str(ex), 500)

class listMembers(Resource):
    @jwt_required()
    def get(self,filters=None):
            # villes = lis.objects()
            # output = ListVilleSchema(many=True).dump(villes)
            try:
                if filters is None:
                    members = Member.objects()
                    output = UserSchema(many=True).dump(members)
                    return success("Succès", {'user':output}, 200)
                else:
                    members = Member.objects(id=filters)
                    output = UserSchema().dump(members)
            except Exception as ex:
                return error("Une erreur est survenue: " + str(ex), 500)

class updateStatus(Resource):
    @jwt_required()
    def put(self,filters=None):
        try:
            body = request.get_json()
            if filters is not None:
                user = User.objects.get(id=filters).update(**body)
                return success("Succès", UserSchema().dump(user), 200)
        except Exception as ex:
            return error("Une erreur est survenue: " + str(ex), 500) 