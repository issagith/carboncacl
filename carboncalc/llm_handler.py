from openai import OpenAI
import pandas as pd
import os

class LLMHandler:
    def __init__(self):
        """Initialise le client OpenAI avec la clé API."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_summary(self, system_prompt, user_prompt, max_tokens=1000, temperature=0.7):
        """
        Interagit avec l'API OpenAI pour générer une réponse basée sur les prompts fournis.
        
        :param system_prompt: Prompt définissant le rôle de l'LLM (contexte général).
        :param user_prompt: Prompt spécifique de l'utilisateur.
        :param max_tokens: Nombre maximum de tokens dans la réponse.
        :param temperature: Niveau de créativité du modèle.
        :return: Résumé généré par le modèle.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Erreur lors de l'interaction avec l'API OpenAI : {e}"
        
    def generate_prompt(self, consumptions):
        """Génère le texte du prompt pour le modèle LLM."""
        df_conso = pd.DataFrame(consumptions)
        total = df_conso['co2_total'].sum() if not df_conso.empty else 0

        summary_text = "Vous êtes un expert en analyse d'empreinte carbone. Ci-dessous les données d'émissions :\n"
        summary_text += f"Total annuel: {total:.2f} kgCO2e\n"

        if not df_conso.empty:
            emissions_by_type = df_conso.groupby('type')['co2_total'].sum().reset_index()
            for _, row in emissions_by_type.iterrows():
                summary_text += f"- {row['type']}: {row['co2_total']:.2f} kgCO2e\n"
        else:
            summary_text += "Aucune consommation enregistrée.\n"

        summary_text += "\nVeuillez fournir une analyse détaillée et personnalisée des émissions et des recommandations pour réduire l'empreinte carbone."
        return summary_text

# Exemple d'utilisation
if __name__ == "__main__":
    llm_handler = LLMHandler()
    system_prompt = "Tu es un assistant spécialisé en environnement et développement durable."
    user_prompt = "Les émissions annuelles de CO2 pour le transport sont de 1200 kgCO2e, pour l'énergie 800 kgCO2e, et pour l'alimentation 600 kgCO2e."
    llm_summary = llm_handler.generate_summary(system_prompt, user_prompt)
    print(llm_summary)
