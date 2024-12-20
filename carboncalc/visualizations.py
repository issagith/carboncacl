import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def convert_to_dataframe(consumptions):
    """Convertit les données en DataFrame si elles sont sous forme de liste."""
    if isinstance(consumptions, list):
        return pd.DataFrame(consumptions)
    return consumptions

def plot_emissions_by_type(consumptions, output_path="emissions_by_type.png"):
    df_conso = convert_to_dataframe(consumptions)
    if df_conso.empty:
        print("Aucune consommation")
        return
    agg = df_conso.groupby('type')['co2_total'].sum().reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=agg, x='type', y='co2_total')
    plt.title("Emissions de CO₂e par type")
    plt.xlabel("Type de poste")
    plt.ylabel("Emissions (kgCO₂e/an)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_emissions_pie(consumptions, output_path="emissions_pie.png"):
    df_conso = convert_to_dataframe(consumptions)
    if df_conso.empty:
        print("Aucune consommation")
        return
    agg = df_conso.groupby('type')['co2_total'].sum().reset_index()
    plt.figure(figsize=(6, 6))
    plt.pie(agg['co2_total'], labels=agg['type'], autopct='%1.1f%%', startangle=90)
    plt.title("Répartition des émissions de CO₂e par type")
    plt.savefig(output_path)
    plt.close()

def plot_top_emitting_products(consumptions, top_n=10, output_path="top_emitting_products.png"):
    df_conso = convert_to_dataframe(consumptions)
    if df_conso.empty:
        print("Aucune consommation")
        return
    top_df = df_conso.groupby('produit')['co2_total'].sum().reset_index().sort_values('co2_total', ascending=False).head(top_n)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=top_df, x='co2_total', y='produit', orient='h')
    plt.title(f"Top {top_n} produits les plus émetteurs")
    plt.xlabel("Emissions (kgCO₂e/an)")
    plt.ylabel("Produit")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_distribution_emissions(consumptions, output_path="distribution_emissions.png"):
    df_conso = convert_to_dataframe(consumptions)
    if df_conso.empty:
        print("Aucune consommation")
        return
    plt.figure(figsize=(8, 5))
    sns.histplot(df_conso['co2_total'], kde=True)
    plt.title("Distribution des émissions par produit")
    plt.xlabel("Emissions (kgCO₂e/an)")
    plt.ylabel("Nombre de produits")
    plt.savefig(output_path)
    plt.close()

def plot_boxplot_emissions_by_type(consumptions, output_path="boxplot_emissions_by_type.png"):
    df_conso = convert_to_dataframe(consumptions)
    if df_conso.empty:
        print("Aucune consommation")
        return
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_conso, x='type', y='co2_total')
    plt.title("Distribution des émissions par type")
    plt.xlabel("Type de poste")
    plt.ylabel("Emissions (kgCO₂e/an)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_quantity_vs_emissions(consumptions, output_path="quantity_vs_emissions.png"):
    df_conso = convert_to_dataframe(consumptions)
    if df_conso.empty:
        print("Aucune consommation")
        return
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df_conso, x='quantite', y='co2_total', hue='type')
    plt.title("Relation entre quantité consommée et émissions")
    plt.xlabel("Quantité annuelle consommée")
    plt.ylabel("Emissions (kgCO₂e/an)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
