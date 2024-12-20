from .llm_handler import LLMHandler
from .visualizations import (
    plot_emissions_by_type,
    plot_emissions_pie,
    plot_top_emitting_products,
    plot_distribution_emissions,
    plot_boxplot_emissions_by_type
)
import pandas as pd
import os

def generate_report(consumptions, output_path="report.html"):
    """Génère un rapport HTML à partir des données de consommation."""
    df_conso = pd.DataFrame(consumptions)
    total = df_conso['co2_total'].sum() if not df_conso.empty else 0

    # Génération des graphiques
    plot_emissions_by_type(consumptions, "emissions_by_type.png")
    plot_emissions_pie(consumptions, "emissions_pie.png")
    plot_top_emitting_products(consumptions, top_n=5, output_path="top_emitting_products.png")
    plot_distribution_emissions(consumptions, "distribution_emissions.png")
    plot_boxplot_emissions_by_type(consumptions, "boxplot_emissions_by_type.png")

    # Appel au modèle LLM via LLMHandler
    llm_handler = LLMHandler()
    prompt = llm_handler.generate_prompt(consumptions)
    system_prompt = "Tu es un assistant spécialisé en environnement et développement durable. Ta réponse doit être une div impérativement ! Fait en sorte qu'elle soit esthétique et bien structurée. N'utilise pas trop de couleurs différentes"
    llm_summary = llm_handler.generate_summary(system_prompt, prompt)

    # Charger le modèle HTML depuis template.txt
    template_path = os.path.join(os.path.dirname(__file__), "template.txt")
    try:
        with open(template_path, "r", encoding="utf-8") as template_file:
            html_template = template_file.read()
    except FileNotFoundError:
        print(f"Erreur : Le fichier template.txt est introuvable à l'emplacement {template_path}.")
        return

    # Remplacer les placeholders dynamiques
    html_content = html_template.format(
        total=total,
        llm_summary=llm_summary,
        emissions_by_type_img="emissions_by_type.png" if os.path.exists("emissions_by_type.png") else "",
        emissions_pie_img="emissions_pie.png" if os.path.exists("emissions_pie.png") else "",
        top_emitting_products_img="top_emitting_products.png" if os.path.exists("top_emitting_products.png") else "",
        distribution_emissions_img="distribution_emissions.png" if os.path.exists("distribution_emissions.png") else "",
        boxplot_emissions_by_type_img="boxplot_emissions_by_type.png" if os.path.exists("boxplot_emissions_by_type.png") else ""
    )

    # Restaurer les accolades pour le CSS
    html_content = html_content.replace("[[", "{").replace("]]", "}")

    # Sauvegarder le rapport
    try:
        with open(output_path, "w", encoding="utf-8") as report_file:
            report_file.write(html_content)
        print(f"Rapport généré dans {output_path}")
    except IOError as e:
        print(f"Erreur lors de l'écriture du rapport : {e}")


