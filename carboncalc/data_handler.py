import pandas as pd
import os

def load_base_carbone(file_path):
    """
    Charger le fichier Base Carbone avec les paramètres spécifiés.

    Args:
        file_path (str): Chemin du fichier Base Carbone.

    Returns:
        pd.DataFrame: Données chargées sous forme de DataFrame.
    """
    return pd.read_csv(
        file_path, 
        sep=';', 
        encoding='latin1', 
        on_bad_lines='skip', 
        quoting=3
    )

def extract_data_by_keywords(df, keywords, forbidden_keywords=[]):
    """
    Renvoie les lignes dans lesquels les mots-clés sont présents dans la colonne "Code de la catégorie" 
    sachant que la colonne code de la category est sous la forme "mot 1 > mot 2, mot 3 > mot 4 ... "
    Vérifie que les mots ne sont pas dans les mots interdits.
    """
    if forbidden_keywords:
        return df[df['"Code de la catégorie"'].str.contains('|'.join(keywords)) & ~df['"Code de la catégorie"'].str.contains('|'.join(forbidden_keywords))]
    else:
        return df[df['"Code de la catégorie"'].str.contains('|'.join(keywords))]



def delete_duplicates(df, column_name):
    """
    Supprime les doublons en se basant sur la colonne spécifiée et assigne la valeur moyenne du CO2 pour chaque produit.

    Args:
        df (pd.DataFrame): DataFrame à nettoyer.

    Returns:
        pd.DataFrame: DataFrame nettoyé sans doublons.
    """

    # Calculer la valeur moyenne du CO2 pour chaque produit sans changer la structure du DataFrame
    df['"Total poste non décomposé"'] = df['"Total poste non décomposé"'].str.replace(',', '.').astype(float)
    df_mean = df.groupby('"Nom base français"')['"Total poste non décomposé"'].transform('mean')
    df['"Total poste non décomposé"'] = df_mean
    return df.drop_duplicates(subset=column_name)

def clean_redundant_quotes(df):
    """
    Supprimer les guillemets redondants des colonnes de texte.

    Args:
        df (pd.DataFrame): DataFrame à nettoyer.

    Returns:
        pd.DataFrame: DataFrame nettoyé.
    """
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.replace(r'"+', '"', regex=True).str.strip('"')
    return df

def rename_column(df, old_column_name, new_column_name):
    """
    Renommer la colonne contenant les émissions de CO2 pour plus de clarté.

    Args:
        df (pd.DataFrame): DataFrame à modifier.
        old_column_name (str): Nom de la colonne à renommer.
        new_column_name (str): Nouveau nom de la colonne.

    Returns:
        pd.DataFrame: DataFrame avec la colonne renommée.
    """
    df.rename(columns={old_column_name: new_column_name}, inplace=True)
    return df

def save_csv(df, file_path):
    """
    Sauvegarder un DataFrame sous forme de fichier CSV.

    Args:
        df (pd.DataFrame): DataFrame à sauvegarder.
        file_path (str): Chemin du fichier CSV.
    """
    df.to_csv(file_path, index=False)

def filter_csvs(base_carbone_path, output_dir):
    """
    Filtrer les données de Base Carbone en trois catégories et sauvegarder les fichiers CSV.

    Args:
        base_carbone_path (str): Chemin du fichier Base Carbone brut.
        output_dir (str): Répertoire où sauvegarder les fichiers filtrés.

    Returns:
        dict: Dictionnaire contenant les chemins des fichiers filtrés.
    """
    # Charger les données
    data_base_carbone = load_base_carbone(base_carbone_path)

    # Supprimer les lignes avec des valeurs manquantes dans la colonne "Code de la catégorie"
    data_base_carbone = data_base_carbone.dropna(subset=['"Code de la catégorie"'])

    # Supprimer les lignes avec des valeurs manquantes dans la colonne "Total poste non décomposé"
    data_base_carbone = data_base_carbone.dropna(subset=['"Total poste non décomposé"'])

    # Garder uniquement les colonnes nécessaires
    columns_common = [
        '"Identifiant de l\'élément"', '"Nom base français"',
        '"Code de la catégorie"', '"Statut de l\'élément"', '"Total poste non décomposé"',
        '"Unité français"', 
    ]
    data_base_carbone = data_base_carbone[columns_common]

    # Mots-clés pour chaque catégorie
    # trouvés en inspectant les valeurs uniques de la colonne "Code de la catégorie"

    keywords_aliments = [
        "Produits agro-alimentaires", "plats préparés", "boissons", "fruits", "légumes",
        "viandes", "lait", "poissons"
    ]
    keywords_energie = ["Gaz naturel", "Solides", "Liquides", "Electricité"]
    forbidden_keywords_energie = ["Usages spéciaux", "Cokes", "aérien", "Archive", "maritime", "fluvial"]
    keywords_equipements = [
        "Electroménager"
    ]

    # Enlever les guillemets redondants
    data_base_carbone = clean_redundant_quotes(data_base_carbone)
    

    # Filtrer les données
    aliments = extract_data_by_keywords(data_base_carbone, keywords_aliments)
    energie = extract_data_by_keywords(data_base_carbone, keywords_energie, forbidden_keywords_energie)
    equipements = extract_data_by_keywords(data_base_carbone, keywords_equipements)


    # Supprimer les doublons
    aliments = delete_duplicates(aliments, '"Nom base français"')
    energie = delete_duplicates(energie, '"Nom base français"')
    equipements = delete_duplicates(equipements, '"Nom base français"')
    
    # Renommer la colonne CO2
    aliments = rename_column(aliments, '"Total poste non décomposé"', 'CO2')
    energie = rename_column(energie, '"Total poste non décomposé"', 'CO2')
    equipements = rename_column(equipements, '"Total poste non décomposé"', 'CO2')

    # Strip les guillemets des noms de colonnes
    aliments.columns = aliments.columns.str.strip('"')
    energie.columns = energie.columns.str.strip('"')
    equipements.columns = equipements.columns.str.strip('"')

    # Garder uniquement les lignes ayant un statu "Valide générique" ou "Valide spécifique"
    aliments = aliments[aliments['Statut de l\'élément'].str.contains('Valide')]
    energie = energie[energie['Statut de l\'élément'].str.contains('Valide')]
    equipements = equipements[equipements['Statut de l\'élément'].str.contains('Valide')]

    # Sauvegarder les fichiers CSV
    os.makedirs(output_dir, exist_ok=True)
    aliments_path = os.path.join(output_dir, 'aliments_extrait.csv')
    energie_path = os.path.join(output_dir, 'energie_extrait.csv')
    equipements_path = os.path.join(output_dir, 'equipements_extrait.csv')

    save_csv(aliments, aliments_path)
    save_csv(energie, energie_path)
    save_csv(equipements, equipements_path)

    print("affichage des valeurs uniques de la colonne 'code de la catégorie' pour les aliments: ")
    print("Aliments: ", aliments['Code de la catégorie'].unique())

    print('Fichiers filtrés sauvegardés avec succès.')
    print("Dimension des données filtrées: ")
    print("Aliments: ", aliments.shape)
    print("Energie: ", energie.shape)
    print("Equipements: ", equipements.shape)

    return {
        'aliments': aliments_path,
        'energie': energie_path,
        'equipements': equipements_path
    }


if __name__ == '__main__':
    base_carbone_path = '../data/Base_carbone.csv'
    output_dir = '../data/'
    filter_csvs(base_carbone_path, output_dir)

