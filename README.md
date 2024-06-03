# CSV Data Visualization
Développement d'une application de visualisation de données CSV avec Streamlit  
Le but est de comprendre les notions de base de Streamlit avec une app fonctionelle  
Ma premiere fois avec github, donc ca va m'aider me familiariser avec l'outil 

## Utilisation
A partir de la console, lancer la commande
```
streamlit run main.py
```

## Versions

**main.py**  
- version initiale de l'application. Cette version correspond au [Lab2](https://github.com/hrhouma/begining_IA_part1/blob/main/lab2.md)
- streamlit utilisé comme frontend
- a chaque fois qu'un fichier es téléchargé, une copie est créée sur le repertoire /data
- l'appercu utilise la fonction dataframe.head(10)
- visualisation de la colonne avec seaborn. Le dataframe est filtré pour afficher seulement les index entre 0 et 180
- y-axis est limité entre 0 et max_value de la colonne * 1.1  

**v2.py**
- version expérimentale 🤪
- permet de télécharger plusieurs fichiers csv au meme temps
- ajouter une liste type case a cocher dans le sidebar pour choisir/enlever un dataset deja chargé   
- au moment de selectionner la colonne, la visualisation l'affiche pour tous les datasets choisis
- selectbox affiche la colonne seulement s'il se trouve dans tous les datasets choisis

## Cher futur moi
- ajouter logging 
- changer l'affichage de l'image en utilisant libraries externes comme ds3.js
- images interactives / scroll pour passer a travers l'axis x sans changer l'echelle