'''
    Laboratoire 2 - A57 Mise en place environnement IA
    @author: Ray Teruya
'''

import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import numpy as np
import seaborn as sns
import os
from pathlib import Path
import csv

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FuncFormatter

#######################################
# PARAMS
#######################################
st.set_page_config(layout="wide")

#######################################
# FONCTIONS
#######################################

#format_yaxis va changer la notation scientifique pour ecriture decimale
#on va s'en servir au moment d'afficher les valeurs dans la visualisation pour l'axis y
def format_yaxis(x, _):
    #return f'{int(x)}'
    return f'{format(float(x), ".3f")}'

#on utilise le decorator @st.cache_data pour ne pas ecrire le fichier a chaque fois que la page change
#si'on appele la fonction avec les memes parametres, il va l'executer seulement la 1ere fois
#Cependant, si le fichier change en contenu mais le nom du fichier change pas, on va malheureusement garder 
#la copie initiale du fichier dans le serveur.
#https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data
@st.cache_data 

#create_file va enregistrer un copie du fichier dans le repertoire /data
#quand on utilise streamlit.file_uploader les donnees sont chargés en memoire donct
#j'aimerais garder une copie
def create_file(filename):
    #Si le dossier 'data' n'existe pas, on va le creer au moment de faire le 1er telechargement     
    root_path = Path(__file__).absolute().parent.parent
    data_path = root_path.joinpath('data')
    if not os.path.exists(data_path): 
        os.makedirs(data_path) 
    df.to_csv(data_path.joinpath(filename),index=False)

#######################################
# SIDEBAR
#######################################
with st.sidebar:
    file = st.file_uploader("Choisissez un fichier CSV", accept_multiple_files=False, type=['csv'])
    st.markdown('''  
            Lab2 - streamlit  
            @author Ray Teruya  
            [github](http://github.com/rteruyas/csv_data_visualization)
            ''')

#######################################
# PAGE PRINCIPALE
#######################################     
if file is not None:
    #Apercu des données avec la fonction head
    try:
        #on va setter la variable separator = None pour force pandas a trouver le separator lui meme
        #ca devrait couvrir les fichier avec ',' et ';'
        df = pd.read_csv(file, sep = None, engine='python', index_col = None)
        st.text(f'Aperçu des données pour {file.name}...')
        st.dataframe(df.head(10))
        create_file(file.name)
        st.text(f'Une copie du fichier a été créée dans le serveur comme /data/{file.name}')  

        numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

        #validation du nombre de colonnes numériques dans le fichier
        #Si le nombre == 0 on affiche de message de warning
        #Cas contraire on utilise selectbox
        #Par default, selectbox va prendre le premier element disponible.
        #On peut changer ca avec l'option index = None + placeholder (message quand il n'a pas de selection)     
        #https://github.com/streamlit/streamlit/issues/949
        #https://stackoverflow.com/questions/7751157/python-csv-list-separator-based-on-regional-settings
        if len(numeric_columns) > 0:
            selected = st.selectbox('Sélectionnez une colonne pour générer un graphique:', numeric_columns, index = None, placeholder = 'Select an option')
            if selected:
                #filtered_df va filtrer les donnees pour la valeur index <= 180
                filtered_df = df.loc[df.index <= 180]      
                fig, ax = plt.subplots(figsize=(30, 8))  
                #Code pour commencer la valeur de y a 0 mais il faut valider que la variable choisie n'a pas de negatif
                #plt.ylim(0, filtered_df[selected].max() * 1.1)
                sns.lineplot(data = filtered_df, x = filtered_df.index, y = selected, ax = ax).set(title=f'Graphique pour la colonne {selected}', xlabel='index', ylabel=selected)
                sns.set_style("whitegrid")
                sns.color_palette(palette='Accent')
                ax.xaxis.set_major_locator(MultipleLocator(10))
                ax.yaxis.set_major_formatter(FuncFormatter(format_yaxis))   
                st.pyplot(fig)
                #st.success('Wohoo! 🎉')
            else:
                st.warning('No option is selected')
        else:
            st.warning(f'{file.name} ne contient pas de colonnes numériques')
    except Exception as e:
        st.text('Erreur avec le téléchargement du fichier. Veuillez essayer avec un autre')
        st.error(e)
else:
    st.markdown('# Application de visualisation de données CSV')
    st.markdown('''
            ### Instructions   
            Pour commencer, veuillez utiliser le menu de gauche pour télécharger un fichier csv.
            ''')