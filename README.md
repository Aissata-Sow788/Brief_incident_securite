# Brief_incident_securite
README – Système de suivi d'incidents (Helpdesk) avec authentification sécurisée
 Contexte
Dans un centre de formation comme Simplon ou UNCHK, les demandes techniques sont fréquentes :
"Mon chargeur ne marche plus"
"Je n'ai pas accès à Simplonline"
"Il me faut un autre ordinateur"
Actuellement, ces demandes arrivent par téléphone, email ou WhatsApp, sans suivi centralisé.

Objectif : Développer une application console sécurisée permettant :
L’authentification des utilisateurs
La création et le suivi des tickets
Une gestion centralisée des demandes
Une traçabilité complète

Architecture du Projet
 Rôles utilisateurs
Apprenant / Staff = user

Créer un compte

Se connecter

Créer un ticket

Consulter ses tickets

Voir le statut de ses demandes

Admin

Toutes les fonctionnalités utilisateur

Voir tous les tickets de la base

Gérer les statuts

Sécurité (Responsabilité Back-End)
La sécurité est une priorité.
Authentification sécurisée
Les mots de passe ne sont jamais stockés en clair


Hashage avec bcrypt

Vérification sécurisée à la connexion

Accès aux tickets uniquement après authentification

Autorisation
Un utilisateur ne peut voir que ses propres tickets

Un admin peut voir tous les tickets

Chaque ticket est lié à son créateur via une clé étrangère

STRUCTURE DE LA BASE DE DONNEE : 
Table tickets:

desc tickets;
+----------------+---------------------------------------+------+-----+------------+----------------+
| Field          | Type                                  | Null | Key | Default    | Extra          |
+----------------+---------------------------------------+------+-----+------------+----------------+
| id_ticket      | int                                   | NO   | PRI | NULL       | auto_increment |
| titre          | varchar(100)                          | NO   |     | NULL       |                |
| description    | varchar(100)                          | NO   |     | NULL       |                |
| niveau_urgence | varchar(100)                          | NO   |     | NULL       |                |
| Statut         | enum('en_attente','en_cour','resolu') | YES  |     | en_attente |                |
| id_user        | int                                   | YES  | MUL | NULL       |                |
+----------------+---------------------------------------+------+-----+------------+----------------+
Table utilisateurs: 

desc utilisateurs;
+----------+----------------------+------+-----+---------+----------------+
| Field    | Type                 | Null | Key | Default | Extra          |
+----------+----------------------+------+-----+---------+----------------+
| id_user  | int                  | NO   | PRI | NULL    | auto_increment |
| Prenom   | varchar(100)         | NO   |     | NULL    |                |
| email    | varchar(100)         | NO   | UNI | NULL    |                |
| password | varchar(100)         | NO   | UNI | NULL    |                |
| role     | enum('admin','user') | YES  |     | user    |                |
+----------+----------------------+------+-----+---------+----------------+

FONCTIONNALITÉS: pour l’Admin

Ajouter ticket
Voir statut de la demande
Afficher tous les tickets
Modifier les rôles
Modifier le statut de la demande
Afficher tous les utilisateurs
Supprimer ticket
Déconnexion

FONCTIONNALITÉS: pour l’Utilisateurs

Ajouter ticket
Consulter son historique de demande
Supprimer ticket
Déconnexion

TECHNOLOGIE UTILISÉE:

Python3
MYSQL
import mysql.connector
import bcrypt

Installation :

pip install mysql-connector-python
pip install bcrypt
LANCER LE PROJET:

Création de la base de donnée:

CREATE DATABASE incident_securite;

Etablir la connexion de la base de donnée dans le code python:
import mysql.connector
import bcrypt
connection = mysql.connector.connect (
           host = ‘localhost’,
           username = ‘root’,
           password = ‘MotDePasseFort’,
           database = ‘incident_securite’
)

vérification de la connexion :
if connection.is_connected:
     print(“Connexion reussi !)

Création de la table tickets:
 create table tickets (
    -> id_ticket int primary key auto_increment,
    -> titre varchar(100) not null,
    -> description varchar(100) not null,
    -> niveau_urgence varchar(100) not null,
    -> Statut enum('en_attente','en_cour','resolu') default 'en_attente',
    -> id_user int,
    -> foreign key (id_user) references utilisateurs(id_user));

création de la table utilisateurs:
 create table tickets (
    -> id_user int primary key auto_increment,
    -> prenom varchar(100) not null,
    -> email varchar(100) not null,
    -> password varchar(100) not null unique,
    -> role enum('admin','user') default 'user',);


Se déconnecter
