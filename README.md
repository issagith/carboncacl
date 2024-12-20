# CarbonCalc

CarbonCalc est un outil Python interactif permettant de calculer et analyser l'empreinte carbone liée à différentes activités. Ce package est conçu pour aider les utilisateurs (notamment les restaurateurs) à évaluer leur impact environnemental en se basant sur des données précises et à générer des rapports visuels.

Note : Ce package est développer dans le cadre d'un projet scolaire avec un temps limité, il est donc possible que certaines fonctionnalités ne soient pas implémentées ou que des bugs soient présents.

## Fonctionnalités

### Création de fichiers de données :
- Génération de fichiers CSV pour les aliments, l'énergie et les équipements.
- Gestion des doublons en faisant des moyennes pondérées des données agrégées.

### Calcul interactif :
- Saisie des consommations liées aux aliments, énergie, et équipements.
- Conversion automatique des données en base annuelle, quel que soit l'intervalle d'entrée (jour, semaine, mois, année).

### Visualisation des données :
- Graphiques générés automatiquement pour comprendre la répartition des émissions.
- Comparaison entre les types de postes de consommation et identification des postes les plus émetteurs.

### Rapport automatisé :
- Génération d'un rapport HTML esthétique et interactif contenant :
    - Résumé des émissions totales.
    - Graphiques visuels.
    - Analyse générée par un modèle de langage (LLM).

## Prérequis

- Python 3.8 ou plus récent
- Clé API OpenAI (pour l'analyse LLM)
- Packages Python : dans le fichier `requirements.txt`

## Installation

Clonez le projet :

```bash
git clone https://github.com/votre-utilisateur/carboncalc.git
cd carboncalc
```

Installez les dépendances grâce au fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

Rendez-vous sur le site d'OpenAI pour obtenir une clé API 

Créez un fichier `.env` à la racine du projet et ajoutez votre clé API :

``` env
OPENAI_API_KEY="votre-clé-api"
```

## Utilisation

Générez les fichiers CSV grâce au module data_handler : 

```bash
python data_handler.py
```

Lancez le programme principal :

```bash
python main.py
```

Suivez les instructions interactives :

- Choisissez un poste de consommation (aliments, énergie, équipements).
- Naviguez par catégories pour sélectionner un produit.
- Obtenez un rapport complet avec graphiques.

Générez un rapport :

- Le rapport est sauvegardé sous forme de fichier HTML (report.html) dans le répertoire de travail.
- Ouvrez-le avec un navigateur pour explorer vos résultats.


## Personnalisation

- **Adapter le modèle LLM** : Modifiez les prompts et les paramètres dans `llm_handler.py` pour personnaliser l’analyse.


## Limitations

- Les données sont limitées aux facteurs d'émission fournis dans les fichiers CSV intégrés.
- L'intégration du modèle LLM nécessite une clé API valide d'OpenAI.

## Auteur
Issa KA