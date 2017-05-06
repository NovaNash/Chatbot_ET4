# Chatbot_ET4
Mickael SERENO, Mathieu LOUVET, Stacy GROMAT

getScripts.py : Permet de récupérer les corpus de films qui nous serviront pour le projet.
./getScripts.py

process.py : Fichier permettant de récupérer les questions / réponses des corpus données en paramètres. Voir le script.py permettant de télécharger les scripts de films. Attention, les scripts doivent avoir le bon format.
			 Le fichier sortant sera dans processed/<filePath>
./process.py file1 [listFile]

projet.py  : Fichier prenant en compte les fichiers qui sont directement dans processed/ pour former sa base de données. Posez vos questions et vous aurez vos réponses.
./projet.py

Dépendances :
    -nltk

