### Prérequis
#pip install flask
#pip install flask_uploads
#pip install werkzeug==0.16.1
#pip install Flask==1.1.4
#pip uninstall markupsafe
#pip install markupsafe==2.0.1

## Import
import bd
# Importe le fichier python qui s'occupe de l'interraction avec la base de donnée

from flask import Flask, render_template, redirect, request ,url_for
# Flask -> pour créer le serveur
# render_template -> pour renvoyer une vue depuis un modèle
# redirect -> pour rediriger vers une autre page
# request -> pour récupérer les informations d'un formulaire (POST ou GET)

from flask_uploads import UploadSet, configure_uploads, IMAGES
# flask_uploads -> pour upload des fichier sur le serveur
# UploadSet -> une class qui permet gérer les fichier
# configure_uploads -> Fonction permetant la liaison avec Flask
# IMAGES -> Un objet fourni par le module qui permet de créer un ensemble d'upload pour les images.


## Serveur flask
# On crée un objet serveur
app = Flask(__name__)


app.config['UPLOADED_PHOTOS_DEST'] = 'static/pkm/' # chemin de destination des fichiers
photos = UploadSet('photos', IMAGES) # créer un ensemble d'upload d'image
configure_uploads(app, photos) # relie l'app  l'ensemble

#On utilise un décorateur (@app.route) pour indiquer au serveur d'exécuter certaines fonctions quand un client demande une page Web.

#Racine du site -> fichier index.html
@app.route('/') # la route correpond à la racine du site
def index():
    """
       Fonction lancée quand le client demande à accéder à la racine du site.
    """
    pkm=bd.HomePKMVedette() # génère les pokémon vedette , qui seront présent dans la page home
    return render_template("index.html",pkm=pkm) # retourne l'index du site


###                                       Fiche de Pokémon
@app.route('/PKM')
def PKM():
    """
       Fonction lancée quand le client demande à accéder à une page d'un pokémon.
    """
    id=request.args.get('id') # récupère l'id qui sera présent en argument
    pkm=bd.infoPKM(id) # récupère les infos du pokémon en fonction de son id
    return render_template("pkm/PKM.html",pkm=pkm)

###                                             Pokédex
@app.route('/pokedex')
def pokedex():
    """
       Fonction lancée quand le client demande à accéder à l'ensemble des pokémon.
    """
    pkm=bd.pokedex() # appelle la fonction pokédex qui retourne l'ensemble des pokémon trié par id
    return render_template("pkm/pokedex.html",pkm=pkm)

###                                            Capacitée
@app.route('/capacite')
def capacite():
    """
       Fonction lancée quand le client demande à accéder à l'ensemble des capacitées présent sur le serveur.
    """
    capa=bd.capacite() # récupère tout les capacitées
    return render_template("capacite/capacitée.html",capa=capa)


@app.route('/capacitePKM')
def capacitePKM():
    """
       Fonction lancée quand le client demande à accéder à l'ensemble des pokémon ayant un capacitée en particulier.
    """
    id=request.args.get('id') # récupère l'id qui sera présent en argument
    capa=bd.capacitePKM(id) # retourne une liste contenant tout les pokémons ayant une capacitée ( selon l'id)
    return render_template("capacite/capacitePKM.html",capa=capa)


###                                             Talent
@app.route('/talent')
def talent():
    """
       Fonction lancée quand le client demande à accéder à l'ensemble des Talents.
    """
    capa=bd.talent() # récupère tout les talents
    return render_template("talent/talent.html",capa=capa)


@app.route('/talentPKM')
def talentPKM():
    """
       Fonction lancée quand le client demande à accéder à l'ensemble des pokémon ayant un talent en particulier.
    """
    id=request.args.get('id') # récupère l'id qui sera présent en argument
    capa=bd.talentPKM(id) # retourne une liste contenant tout les pokémons ayant une capacitée ( selon l'id)
    return render_template("talent/talentPKM.html",capa=capa)


###                                        HUB Upload
@app.route('/upload')
def uploadHub():
    """
       Fonction lancée quand le client demande à accéder au menu des différents Upload.
    """
    return render_template("upload/upload.html") # affiche le menu des uploads

###                                       Upload Talent
@app.route('/uploadtalent')
def uploadTalent():
    """
       Fonction lancée quand le client demande à accéder au formulaire d'ajout de talent.
    """
    verif=True# initie une variable
    # vérifie si on lui  envoyé un argument ( présent dans l'url)
    if request.args.get('id')!= None:
        verif=False# passe la variable à false
    return render_template("upload/upload/uploadtalent.html",verif=verif)

# Action exécutée quand on clique sur le bouton submit pour ajouter un talent
@app.route('/nvTalent', methods = ['POST'])
def upTalent():
    """
       Fonction qui récupère les informations d'un formulaire concernant l'ajout d'un talent et les ajoute dans la base de données.
    """
    talent = request.form # récupère les info données dans le formulaire et les met de dico
    verif=True
    # vérifie si chacun des éléments à été rempli
    if not talent['nom']or not talent['effet'] :
        verif= False # si non , il met la variable verif en False

     # si il manque des éléments
    if verif==False:
        return redirect("/uploadtalent?id=False") # retourne une page avec un message d'erreur
    # si tout les champs du formulaire ont été rempli
    else:
        bd.ajouttalent(talent['nom'],talent['effet']) # lance la fonction ajoutant un Talent
        return redirect("/talent")


###                                    Upload Capacitée
@app.route('/uploadcapacite')
def uploadcapacite():
    """
       Fonction lancée quand le client demande à accéder au formulaire d'ajout de capacitée.
    """
    type=bd.type()
    verif=True # initie une variable
    # vérifie si on lui  envoyé un argument ( présent dans l'url)
    if request.args.get('id')!= None:
        verif=False # passe la variable à false
    return render_template("upload/upload/uploadcapacite.html",type=type,verif=verif)

# Action exécutée quand on clique sur le bouton submit pour ajouter une capacitée
@app.route('/nvCapa', methods = ['POST'])
def upCapacite():
    """
       Fonction qui récupère les informations d'un formulaire concernant l'ajout d'une capacitée et les ajoute dans la base de données.
    """
    Capa = request.form # récupère les info données dans le formulaire et les met de dico
    verif=True
    # vérifie si chacun des éléments à été rempli
    if not Capa['nom']or not Capa['Type']or not Capa['Degat']or not Capa['Precison']or not Capa['Description'] :
        verif= False # si non , il met la variable verif en False


    # si il manque des éléments
    if verif==False:
        return redirect("/uploadcapacite?id=False") # retourne une page avec un message d'erreur
    # si tout les champs du formulaire ont été rempli
    else:
        bd.ajoutcapacitee(Capa['nom'],Capa['Type'],Capa['Degat'],Capa['Precison'],Capa['Description']) # lance la fonction ajoutant une capacitée
        return redirect("/capacite")



###                                    Upload Pokémon
@app.route('/uploadPKM')
def uploadPKM():
    """
       Fonction lancée quand le client demande à accéder au formulaire d'ajout de pokémon.
    """
    type=bd.type() # récupère les types pour les utiliser dans un menu déroullant
    verif=True # initie une variable
    # vérifie si on lui  envoyé un argument ( présent dans l'url)
    if request.args.get('id')!= None:
        verif=False #passe la variable à false
    return render_template("upload/upload/uploadpkm.html",type=type,verif=verif)

# Action exécutée quand on clique sur le bouton submit pour ajouter un pokémon
@app.route('/nvPKM', methods = ['POST'])
def upPKM():
    """
       Fonction qui récupère les informations d'un formulaire concernant l'ajout d'un pokémon et les ajoute dans la base de données.
    """
    PKM = request.form # récupère les info données dans le formulaire et les met de dico
    file = request.files['photos'] # récupère l'image
    verif=True
    # vérifie si chacun des éléments à été rempli
    if not PKM['num'] or not PKM['nom']or not PKM['Type']or not PKM['hp']or not PKM['atk']or not PKM['def']or not PKM['spe'] or not file or not bd.requeteSQL("SELECT sprite FROM Pokemon WHERE Pokedex_national= ? ;",(PKM['num'],))== []:
        verif= False # si non , il met la variable verif en False

    # si il manque des éléments
    if verif==False:
        return redirect("/uploadPKM?id=False") # retourne une page avec un message d'erreur
    # si tout les champs du formulaire ont été rempli
    else:
        filename = photos.save(file) # sauveguarde l'image dans le serveur

        # récupère le nom et lui ajoute son chemin
        filen=file.filename
        filen="static/pkm/"+filen
        replace_spaces = lambda s: s.replace(' ', '_')
        filen = replace_spaces(filen)


        PKM = request.form # récupère les info données dans le formulaire et les met de dico
        bd.ajoutpkm(filen,PKM['num'],PKM['nom'],PKM['Type'],PKM['hp'],PKM['atk'],PKM['def'],PKM['spe'])# lance la fonction ajoutant un pokémon
        a="/PKM?id="+str(PKM['num']) # génère un lien vers la page d'information de ce pokémon
        bd.resize_image(filen)
        return redirect(a) # redirige vers le pokémon ajouter

###                                   Assigner Talent
@app.route('/assignerTalent')
def assignerTalent():
    """
       Fonction lancée quand le client demande à accéder au formulaire d'assignation de talent.
    """
    i=bd.talent() # fait appelle à la fonction qui renvoie tout les talent
    a=bd.pokedex() # fait appelle à la fonction qui renvoie tout les pokémon
    tal=[a,i] # créer un liste contenant les pokémon ainsi que les talents
    return render_template("upload/assignation/assignertalent.html",tal=tal)

# Action exécutée quand on clique sur le bouton submit pour assigner le Talent
@app.route('/asTalent', methods = ['POST'])
def asTalent():
    """
       Fonction qui récupère les informations d'un formulaire concernant l'assignation de Talent et les ajoute dans la base de données.
    """
    talent = request.form # récupère les info données dans le formulaire et les met de dico
    bd.assignertal(talent['pkm'],talent['Talent']) # fait appelle  la fonction assignant un talent dans la table
    return redirect("/")


###                                Assigner capacitée
@app.route('/assignerCapacite')
def assignerCapacite():
    """
       Fonction lancée quand le client demande à accéder au formulaire d'assignation de capacitée.
    """
    i=bd.capacite() # fait appelle à la fonction qui renvoie tout les capacitées
    a=bd.pokedex() # fait appelle à la fonction qui renvoie tout les pokémon
    tal=[a,i] # créer un liste contenant les pokémon ainsi que les capacitées
    return render_template("upload/assignation/assignercapaciter.html",tal=tal)

# Action exécutée quand on clique sur le bouton submit pour assigner la capacitée
@app.route('/asCapa', methods = ['POST'])
def asCapa():
    """
       Fonction qui récupère les informations d'un formulaire concernant l'assignation de capacitée et les ajoute dans la base de données.
    """
    talent = request.form # récupère les info données dans le formulaire et les met de dico
    bd.assignercapa(talent['pkm'],talent['Capa']) # fait appelle  la fonction assignant la capacitée dans la table
    return redirect("/")

###                                Assigner sous évolution
@app.route('/assignerSOUS')
def assignerSOUS():
    """
       Fonction lancée quand le client demande à accéder au formulaire d'assignation de sous évolution.
    """
    a=bd.pokedex() # fait appelle à la fonction qui renvoie tout les pokémon
    tal=[a,] # créer un liste contenant les pokémon
    return render_template("upload/assignation/ass-.html",tal=tal)

# Action exécutée quand on clique sur le bouton submit pour assigner la sous évolution
@app.route('/asSOUS', methods = ['POST'])
def asSOUS():
    """
       Fonction qui récupère les informations d'un formulaire concernant l'assignation de sous évolution et les ajoute dans la base de données.
    """
    talent = request.form # récupère les info données dans le formulaire et les met de dico
    bd.sous(talent['pkm'],talent['sous']) # fait appelle  la fonction ajoutant l'évolution dans la table
    return redirect("/")

###                                Assigner sur évolution
@app.route('/assignerSUR')
def assignerSUR():
    """
       Fonction lancée quand le client demande à accéder au formulaire d'assignation de sur évolution.
    """
    a=bd.pokedex() # fait appelle à la fonction qui renvoie tout les pokémon
    tal=[a,] # créer un liste contenant les pokémon
    return render_template("upload/assignation/ass+.html",tal=tal)

# Action exécutée quand on clique sur le bouton submit pour assigner la sur évolution
@app.route('/asSUR', methods = ['POST'])
def asSUR():
    """
       Fonction qui récupère les informations d'un formulaire concernant l'assignation de sur évolution et les ajoute dans la base de données.
    """
    talent = request.form # récupère les info données dans le formulaire et les met de dico
    bd.sur(talent['pkm'],talent['sur']) # fait appelle  la fonction ajoutant l'évolution dans la table
    return redirect("/")





### On lance le serveur (il sera local ici, accessible à l'adresse http://127.0.0.1:5000 )
app.run(debug=True)