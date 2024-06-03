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

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FuncFormatter

st.set_page_config(layout="wide")

def format_yaxis(x, _):
    return f'{int(x)}'

with st.sidebar:
    file = st.file_uploader("Choisissez un fichier CSV", accept_multiple_files=False, type=['csv'])
    st.markdown('''  
            Lab2 - streamlit  
            author: Ray Teruya  
            [github repository](http://github.com/rteruyas/csv_data_visualization)
            ''')
     
if file is not None:
    #### Lecture du fichier téléchargé
    #Apercu des données avec la fonction head
    df = pd.read_csv(file)
    st.text(f'Aperçu des données pour {file.name}...')
    st.dataframe(df.head(10))
    #st.dataframe(df.sample(10))

    #### Création d'une copie dans le serveur
    #La fonction file_uploader garde le fichier en memoire (RAM) pour l'utiliser au besoin 
    #J'aimerais garder une copie de chaque fichier traité dans le repertoire 'repo'
    #Si le dossier data n'existe pas, on va le creer au moment de faire le 1er telechargement     
    if not os.path.exists("../data"): 
        os.makedirs("../data") 

    df.to_csv("../data" + "/" + file.name)
    st.text(f'Une copie physique a été créée dans le serveur comme ./data/{file.name}')  

    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

    ### validation du nombre de colonnes numériques dans le fichier
    #Si le nombre == 0 on affiche de message de warning
    #Cas contraire on utilise selectbox
    #Par default, selectbox va prendre le premier element disponible.
    #On peut changer ca avec l'option index = None + placeholder (message quand il n'a pas de selection)     
    #Reference: https://github.com/streamlit/streamlit/issues/949
    if len(numeric_columns) > 0:
        selected = st.selectbox('Sélectionnez une colonne pour générer un graphique:', numeric_columns, index = None, placeholder = 'Select an option')
        if selected:
            #filtered_df va filtrer les donnees pour la valeur index <= 180
            filtered_df = df.loc[df.index <= 180]      
            fig, ax = plt.subplots(figsize=(30, 8))  
            plt.ylim(0, df[selected].max() * 1.1)
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
else:
    st.markdown('# Application de visualisation de données CSV')
    st.markdown('''
            ### Instructions   
            Pour commencer, veuillez utiliser le menu de gauche pour télécharger un fichier csv.
            ''')