import mysql.connector
import bcrypt


connection = mysql.connector.connect(
    host = "localhost",
    username = "root",
    password = "MotDePasseFort",
    database = "incident_securite"
)

if connection.is_connected():
    print("Connexion reuissi !")

#================================MENU ADMIN===========================================================

def menu_admin():
    print("==========================MENU ADMIN=================================")
    print("1: Ajouter ticket")
    print("2: Voir l'etat de la demande")
    print("3: Afficher les tickets")
    print("4: Modifier les roles")
    print("5: Modifier les status de la demande")
    print("6: Afficher les utilisateurs")
    print("7: Supprimer tickets")
    print("0: Deconnexion")
    print("=====================================================================")

#========================================MENU USER===============================================

def menu_user():
    print("==========================MENU USER==================================")
    print("1: Ajouter un ticket")
    print("2: Consulter son historique demande")
    print("3: supprimer ticket")
    print("0: Deconnexion")
    print("======================================================================")

    while True:
        choix = input("Entrez votre choix:")
        if choix == "1":
            ajout_ticket()
        elif choix == "2":
            historique_demandes_user()
        elif choix == "3":
            supprimer_tickets_use()
        elif choix == "0":
            authentification()
        else:
            print("Erreur")

#=========================================INSCRIPTION=====================================================
    
def inscription():
    prenom = input("Entrez votre prenom:")
    if not prenom.isalpha():
        print("Erreur de saisie")
        return
    
    email = input("Entrez votre mail:")

    password = input("Entrez votre mot de passe:")

    if not len(password) <= 8:
        print("Veuiller saisir un mdp avec 8 caractere !")
   

    password_byte = password.encode('utf-8')
    hasher = bcrypt.hashpw(password_byte, bcrypt.gensalt())


    cursor = connection.cursor()
    query = "insert into utilisateurs (prenom, email, password, role) values (%s, %s, %s, %s)"
    cursor.execute(query, (prenom, email, hasher, 'user'))
    connection.commit()
    print(f"Bienvenue {prenom}")
    authentification()

    cursor.close()

#==================================================SUPPRIMER TICKET================================================

def supprimer_tickets():
    afficher_ticket()
    id_ticket = input("Entrez l'id du ticket que vous voudrais supprimer:")
    if not id_ticket.isdigit():
        print("Erreur de saisie !")
        return
    
    cursor = connection.cursor()
    query = "delete from tickets where id_ticket = %s"
    cursor.execute(query)
    connection.commit()
    print(f"{id_ticket} est bien supprimer")
    choix_menu()

    cursor.close()

#=============================================SUPPRIMER UTILISATEURS=================================================
def supprimer_user():
    id_user = input('Entrez id utilisateur que tu veux supprimer:')
    cursor = connection.cursor()
    query = 'delete from utilisateurs where id_user = %s'
    cursor.execute(query, (id_user,))
    connection.commit()
    print(f"{id_user} est bien supprimer !")


#============================================SUPPRIMER TICKET USE=====================================================

def supprimer_tickets_use():

    id_use = input("Entre ton identifiant:")
    if not id_use.isdigit():
        print("Erreur de saisie !")
        return
    cursor = connection.cursor()
    query = "select u.id_user, u.prenom, t.id_ticket, t.titre, t.description, t.niveau_urgence, t.statut from  utilisateurs u inner join tickets t on u.id_user = t.id_user where u.id_user = %s group by u.id_user, u.prenom, t.id_ticket, t.titre, t.description, t.niveau_urgence, t.statut "
    cursor.execute(query, (id_use,))
    for row in cursor.fetchall():
         print(f"id_user: {row[0]} | prenom: {row[1]} | id_ticket: {row[2]} | titre: {row[3]} | niveau_urgence: {row[4]} | statut: {row[5]} | ")

    id_ticket = input("Entrez l'id du ticket que vous voudrais supprimer:")
    if not id_ticket.isdigit():
        print("Erreur de saisie !")
        return
    
    cursor = connection.cursor()
    query = "delete from tickets where id_ticket = %s"
    cursor.execute(query, (id_ticket,))
    connection.commit()
    print(f"{id_ticket} est bien supprimer")
    menu_user()

    cursor.close()

#====================================================AFFICHER UTILISATEUR===============================================

def afficher_utilisateur():
    cursor = connection.cursor()
    query = "select * from utilisateurs"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"id_user: {row[0]} | prenom: {row[1]} | email: {row[2]} | passwors: {row[3]} | role: {row[4]}")

    cursor.close()

#=============================================UPDATE STATUT================================================================

def update_statut():

    id_ticket = input("Entrez id ticket:")
    if not id_ticket.isdigit():
        print("Erreur de saisie !")
        return
    
    statut = input("Entrez le nouveau statut:")
    if not statut.isalpha():
        print("saisie incorrect")
        return
    
    cursor = connection.cursor()

    
    query = "update tickets set statut = %s where id_ticket = %s"
    cursor.execute(query, (statut, id_ticket))
    connection.commit()
    print("Statut mise a jour avec succes !")

    choix_menu()
    
    cursor.close()

#==========================================AJOUTER TICKET=======================================================

def ajout_ticket():
    id_use = input("Entre ton identifiant:")

    try:
        titre_ticket = input("Entrez le titre:")
        if len(titre_ticket) < 2:
            print("Titre invalide")
            return
       
        
        description = input("Entrez description:")
        if len(description) < 2:
            print("Description invalide")
            return
        
        
        niveau_urgence = input("Entrez niveau urgence:")
        if len(niveau_urgence) < 2:
            print("Description invalide")
            return 
        

        id_utilisateur = input("Entrez l'id utilisateur:")
        if not id_utilisateur.isdigit():
            print("Erreur de saisie !")
            return
        if not id_utilisateur == id_use:
            print("id invalide")
            return
        
        cursor = connection.cursor()

        query = "insert into tickets (titre, description, niveau_urgence, statut, id_user) values (%s, %s, %s, %s, %s)"
        cursor.execute(query, (titre_ticket, description, niveau_urgence, 'en_attente', id_utilisateur))
        connection.commit()
        print("Ticket ajouté avec succès !")
        menu_user()

    except Exception as e:
        print("Erreur:",e)

    cursor.close()

#=================================================HISTORIQUE DEMANDES=======================================================
    

def historique_demandes_user():
    id_use = input("Entre ton identifiant:")
    if not id_use.isdigit():
        print("Erreur de saisie !")
        return
    cursor = connection.cursor()
    query = "select u.id_user, u.prenom, t.id_ticket, t.titre, t.description, t.niveau_urgence, t.statut from  utilisateurs u inner join tickets t on u.id_user = t.id_user where u.id_user = %s group by u.id_user, u.prenom, t.id_ticket, t.titre, t.description, t.niveau_urgence, t.statut "
    cursor.execute(query, (id_use,))
    for row in cursor.fetchall():
         print(f"id_user: {row[0]} | prenom: {row[1]} | id_ticket: {row[2]} | titre: {row[3]} | niveau_urgence: {row[4]} | statut: {row[5]} | ")
    menu_user()

    cursor.close()

#=============================================MISE A JOUR ROLE==============================================================

def update_role():
    role_user = input("Entrez le nouveau role:")
    if not role_user.isalpha():
        print("saisie incorrect")
        return 
    
    id_user = input("Entrez le id user:")
    if not id_user.isdigit():
        print("Erreur de saisie !")
        return

    
    cursor = connection.cursor()

    query = "update utilisateurs set role = %s where id_user = %s"
    cursor.execute(query, (role_user, id_user))
    connection.commit()
    
    if cursor.rowcount > 0:
        print("Rôle mis à jour avec succès.")
    else:
        print("Aucun utilisateur trouvé avec cet ID.")

    choix_menu()

    cursor.close()

#==================================================AFFICHER TICKETS============================================================

def afficher_ticket():
    cursor = connection.cursor()
    query = "select * from tickets"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"id_ticket: {row[0]} | titre: {row[1]} | description: {row[2]} | niveau_urgence: {row[3]} | statut: {row[4]} | id_user: {row[5]}")

        cursor.close()

#============================================VOIR ETAT DEMANDE===============================================================

def voir_etat():
    cursor = connection.cursor()
    query = "select id_ticket, titre, statut from tickets"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"id_ticket: {row[0]} | titre: {row[1]} | statut: {row[2]}")

    cursor.close()

#=========================================CHOIX MENU====================================================================

def choix_menu():
    
    while True:
        menu_admin()
        choix = input("Entrez votre choix:")
        if choix == "1":
            ajout_ticket()
        elif choix == "2":
            voir_etat()
        elif choix == "3":
            afficher_ticket()
        elif choix == "4":
            update_role()
        elif choix == "5":
            update_statut()
        elif choix == "6":
            afficher_utilisateur()
        elif choix == "7":
            supprimer_tickets()
        elif choix == "0":
            authentification()
        else:
            print("Erreur")

#==================================================LOGIN=======================================================

def login():

    email = input("Entrez votre mail:")
    cursor = connection.cursor()
    query = "select password, role from utilisateurs where email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    if not result:
        print("Email incorrect")
        return

    password = input("Entrez votre mdp:")
    if not len(password) <= 8:
        print("Veuiller saisir un mdp avec 8 caractere !")
        return
   
    password_byte = password.encode('utf-8')
    hasher_user = result[0].encode('utf-8')
    role = result[1]

    if bcrypt.checkpw(password_byte, hasher_user):
        print("Connexion reuissi !")
        print("role", role)

        if role == 'admin':
            choix_menu()
        elif role == 'user':
            menu_user()
    else:
        print("Mot de passe incorrect")
    
    cursor.close()

#============================================AUTHENTIFICATION=====================================================================

def authentification():
    print("===========================CONNEXION==============================")
    print("1: INSCRIPTION")
    print("2: SE CONNECTER")

    while True:
        choix = input("Entrez votre choix:")
        if choix == "1":
            inscription()
        elif choix == "2":
            login()
        else:
            print("Erreur")

authentification()

connection.close()




