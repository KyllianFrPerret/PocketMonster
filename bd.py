import sqlite3
from random import sample
from PIL import Image
###                                           Requête SQL
def requeteSQL(requete,parametres = None,base='Pocket-Monster'):
    """
        Fonction de requête sur une base sqlite3.
        Entrée:
            requete -> correspond à la requete ( en str) qu'on va éxecuter
            parametres -> si la requete nécessite des paramètres , on les met ici dans un tuple/ sert à éviter les injections sql
            base -> on a assigner par défault notre base de données
        Sortie:
            liste -> renvoie le résultat de la requête sous forme de liste de liste
    """
    # on ouvre la bas de données , on creée un curseur
    con = sqlite3.connect(base)
    con.isolation_level = None
    cur = con.cursor()

    # si il y'a pas de paramètre , on l'execute sans
    if parametres == None:
        cur.execute(requete)
    # sinon on execute avec les paramètres
    else:
        cur.execute(requete,parametres)
    res = cur.fetchall() # on récupère le résultat de la requête

    # ferme l'&ccès à la base de données
    cur.close()
    con.close()

    # transforme le résultat de la requète en liste de liste
    liste = []
    for resu in res:
        liste.append(list(resu))
    return liste


###Taille image


def resize_image(image_path, target_width=256, target_height=256):
    # Ouvrir l'image avec PIL
    image = Image.open(image_path)

    # Obtenir les dimensions actuelles de l'image
    current_width, current_height = image.size

    # Vérifier si les dimensions sont différentes de la cible
    if current_width != target_width or current_height != target_height:
        # Calculer les dimensions de recadrage
        left = (current_width - target_width) / 2
        top = (current_height - target_height) / 2
        right = (current_width + target_width) / 2
        bottom = (current_height + target_height) / 2

        # Recadrer l'image
        cropped_image = image.crop((left, top, right, bottom))

        # Enregistrer l'image recadrée
        cropped_image.save(image_path)
















###                                             HOME
def HomePKMVedette():
    '''
        Renvoie une liste de 5 pokémon qui seront présent sur la page d'acceuil
    '''
    # récupère tous les pokémon avec leur sprite, leur nom et leur id
    requete='SELECT sprite, Pokedex_national ,nom FROM Pokemon ;'
    a=requeteSQL(requete)
    # en choisis 5 aléatoirement
    b=sample(a, 5)
    return b


###                                       Pokémon Info
def infoPKM(id):
    '''
        Fonction qui renvoie toute les information d'un pokémon ( capacitée, talent , évolution,...)
        Entrée:
            id -> l'id du pokémon choisi
        Sortie:
            pkm -> renvoie toutes ces infos dans une liste

    '''
    # récupère toutes les info d'un pokémon contenue dans la table Pokemon en fonction de l'id demander
    requete='SELECT * FROM Pokemon WHERE Pokedex_national = ? ;'
    id=(id,)
    a=requeteSQL(requete,id)

    # récupère les évolutions du pokémon
    evo=evolution(id)
    a.append(evo)# les ajoute à la liste

    # récupère les infos du talents du pokémon
    requete="SELECT * FROM Talent WHERE tal= ?"
    para=(a[0][4],)
    d=requeteSQL(requete,para)
    # si la requête renvoie rien
    if d==[]:
        a.append([None,None])# ajoute une liste vide
    #sinon ajoute les infos du talent
    else:
        a.append(d)

    # récupère toute les capacitée du pokémon
    requete='SELECT Capacite.id_capa,Capacite.Nom,Capacite.Type,Capacite.Degat,Capacite.Précision,Capacite.Description FROM Pokemon JOIN Assignation ON Pokemon.Pokedex_national = Assignation.id_p JOIN Capacite ON Assignation.id_c = Capacite.id_capa WHERE Pokedex_national= ? ;'
    b=requeteSQL(requete,id)
    a.append(b)# ajoute ses capacitée à la liste
    pkm=a
    return pkm


def evolution(id):
    '''
        Renvoie les évolutions d'un pokémon en fonction de son id
        Entrée:
            id -> l'id du pokémon
        Sortie:
            y -> une liste contenant ses évolutions si il en a
    '''
    y=[] # variable qu'on va renvoyer

    # Verifie/Récupère les info de la sous évolution
    requete='SELECT Sous_evo.Sous_pkm FROM Pokemon JOIN Sous_evo ON Pokemon.Pokedex_national = Sous_evo.Num_pkm WHERE Sous_evo.Num_pkm = ?  ;'
    a=requeteSQL(requete,id)
    #si il renvoie un pokémon
    if a!=[]:
        # va rechercher les info ( sprite , nom et id) et les ajouter à la liste
        idp=a[0][0]
        requete='SELECT sprite , Pokedex_national, nom FROM Pokemon WHERE Pokedex_national= ? ;'
        idp=(idp,)
        sous=requeteSQL(requete,idp)
        y.append(sous[0])
    # sinon ajoute une liste vide
    else:
        y.append([])

    # Verifie/Récupère les info de la sur évolution
    requete='SELECT Sur_evo.Sur_pkm FROM Pokemon JOIN Sur_evo ON Pokemon.Pokedex_national = Sur_evo.Num_pkm WHERE Sur_evo.Num_pkm = ?  ;'
    a=requeteSQL(requete,id)
    #si il renvoie un pokémon
    if a!=[]:
        # va rechercher les info ( sprite , nom et id) et les ajouter à la liste
        idp=a[0][0]
        requete='SELECT sprite , Pokedex_national, nom FROM Pokemon WHERE Pokedex_national= ? ;'
        idp=(idp,)
        sur=requeteSQL(requete,idp)
        y.append(sur[0])
     # sinon ajoute une liste vide
    else:
        y.append([])
    return y


def type():
    '''
        Renvoie la liste de tout les types
    '''
    requete="SELECT * FROM Type"
    a=requeteSQL(requete)
    return a

###                                            Pokédex
def pokedex():
    '''
        Renvoie une liste de tout les pokémon par ordre d'id
    '''
    requete='SELECT sprite, Pokedex_national,nom,type FROM Pokemon ORDER BY Pokedex_national ASC ;'
    ret=requeteSQL(requete)
    return ret

###                                             Upload
def ajouttalent(talent,effet):
    '''
        Fonction qui prend en entrée 2 paramètres et les ajoute dans la table Talent
        Entrée:
            talent -> non du talent (str)
            effet -> effet du talent (str)
    '''
    requete="INSERT INTO Talent VALUES (?,?)"
    para=(talent,effet)
    requeteSQL(requete,para)

def ajoutcapacitee(Nom,Type,Degat,Precision,Description):
    '''
        Fonction qui prend en entrée 5 paramètres et les ajoute dans la table Capacitee
        Entrée:
            Nom -> non de la capacitée (str)
            Type -> type de la capacitée (str)
            Degat -> Degat infligée de la capacitée (str)
            Precision -> Precision de la capacitée (str)
            Description -> Description de la capacitée (str)
    '''
    # récupère l'id maw
    requete1="SELECT max(id_capa) FROM Capacite;"
    id=requeteSQL(requete1)
    id=id[0][0]+1 # incrémente l'id prècedante
    # insèrer la capacitée
    requete="INSERT INTO Capacite VALUES (?,?,?,?,?,?)"
    para=(id,Nom,Type,Degat,Precision,Description)
    requeteSQL(requete,para)



def ajoutpkm(sprite,num,nom,type,hp,atk,deff,spe):
    '''
        Fonction qui prend en entrée 8 paramètres et les ajoute dans la table Pokemon
        Entrée:
            sprite -> sprite du Pokémon (str)
            num -> id du pokedex_national du Pokémon (str)
            Nom -> non du Pokémon (str)
            type -> type du Pokémon (str)
            hp -> pv du Pokémon (str)
            atk -> attaque du Pokémon (str)
            deff -> défense du Pokémon (str)
            spe -> vitesse du Pokémon (str)
    '''
    # insère le pokémon
    requete="INSERT INTO Pokemon (sprite,Pokedex_national, Nom,Type,HP,ATK,DEF,SPE) VALUES (?,?,?,?,?,?,?,?)"
    para=(sprite,num,nom,type,hp,atk,deff,spe)
    requeteSQL(requete,para)
    # insère la capacité Protection ( capacitée que tout les pokémon peuvent apprendre)
    requete="INSERT INTO Assignation VALUES (?,?)"
    para=(num,0)
    requeteSQL(requete,para)

###                                          Assignation
def assignertal(id,tal):
    '''
        Ajouté dans la table assignation , une id de pokémon et une id de talent
        Entrée:
            id -> id du pokémon
            tal -> id du talent
    '''
    # insère dans la ligne du pokémon dans la table Pokemon
    requete1="UPDATE Pokemon SET Talent= ? WHERE Pokedex_national = ?;"
    para=(tal,id)
    id=requeteSQL(requete1,para)



def assignercapa(id,capa):
    '''
        Ajouté dans la table assignation , une id de pokémon et une id de la capacitée
        Entrée:
            id -> id du pokémon
            capa -> id de la capacitée
    '''
    # insère dans assigation
    requete1="INSERT INTO Assignation VALUES (?,?);"
    para=(id,capa)
    id=requeteSQL(requete1,para)

###                                           Évolution
def sous(id,sous):
    '''
        Ajouté dans la table Sous_evo , une id de pokémon et l'id de sa sous évolution
        Entrée:
            id -> id du pokémon
            sous -> id de la sous évolution
    '''
    # insère dans Sous_evo
    requete1="INSERT INTO Sous_evo VALUES (?,?);"
    para=(id,sous)
    id=requeteSQL(requete1,para)

def sur(id,sur):
    '''
        Ajouté dans la table Sur_evo , une id de pokémon et l'id de son évolution suivante
        Entrée:
            id -> id du pokémon
            sur -> id de la sur évolution
    '''
    # insère dans Sur_evo
    requete1="INSERT INTO Sur_evo VALUES (?,?);"
    para=(id,sur)
    id=requeteSQL(requete1,para)

###                                           Capacitée
def capacite():
    '''
        Renvoie une liste de toutes les capacitée et leurs effets
    '''
    # requête sql
    requete='SELECT * FROM Capacite;'
    ret=requeteSQL(requete)
    return ret

def capacitePKM(id):
    '''
        Récupère une liste de pokémon ayant une même capacité en fonction de l'id de la capacitée
        Entrée:
            id -> id de la capacitée
        Sortie:
            retu -> liste de pokémon
    '''
    # join la table pokemon et assignation pour récuper les pokémon ayant été assigner avec l'id
    id=(id,)
    requete='SELECT Pokemon.sprite, Pokemon.Pokedex_national,Pokemon.nom,Pokemon.type FROM Pokemon JOIN Assignation ON Pokemon.Pokedex_national=Assignation.id_p WHERE Assignation.id_c= ? ORDER BY Pokemon.Pokedex_national ASC ;'
    ret=requeteSQL(requete,id)
    # récupère les infos de la capacitée
    requete='SELECT * FROM Capacite WHERE id_capa= ?;'
    a=requeteSQL(requete,id)
    retu=[a,ret]
    return retu

###                                            Talent
def talent():
    '''
        Renvoie une liste de tout les talents ainsi que leur effet
    '''
    # requête sql
    requete1="SELECT * FROM Talent;"
    id=requeteSQL(requete1)
    return id

def talentPKM(id):
    '''
        Récupère une liste de pokémon ayant un même talent en fonction du nom de la capacitée entrée
        Entrée:
            id -> nom du talent
        Sortie:
            re -> liste de pokémon
    '''
     # récupère tout les pokémon ayant le talent
    id=(id,)
    requete='SELECT sprite, Pokedex_national,nom,type FROM Pokemon WHERE Talent= ? ORDER BY Pokedex_national ASC ;'
    ret=requeteSQL(requete,id)
    # récupère les infos du talent
    requete='SELECT * FROM Talent WHERE Tal = ?;'
    a=requeteSQL(requete,id)
    re=[a,ret]
    return re
