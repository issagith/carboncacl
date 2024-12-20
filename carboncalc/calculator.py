class CarbonCalculator:
    def __init__(self, df_aliments, df_energie, df_equipements):
        self.df_aliments = df_aliments
        self.df_energie = df_energie
        self.df_equipements = df_equipements

        # Harmonisation des noms
        for df in [self.df_aliments, self.df_energie, self.df_equipements]:
            df["Nom base français"] = df["Nom base français"].astype(str).str.lower()

        self.consumptions = []
        self.hierarchies = {
            'aliments': self.build_hierarchy(self.df_aliments),
            'energie': self.build_hierarchy(self.df_energie)
        }

        self.period = None
        self.period_factor = 1

    def set_period(self, period_choice):
        """
        period_choice: str in {'jour','semaine','mois','année'}

        Cette méthode ne demande plus directement à l'utilisateur,
        mais on lui passera la valeur depuis main.py.
        """
        if period_choice == 'jour':
            self.period = 'jour'
            self.period_factor = 365
        elif period_choice == 'semaine':
            self.period = 'semaine'
            self.period_factor = 52
        elif period_choice == 'mois':
            self.period = 'mois'
            self.period_factor = 12
        elif period_choice == 'année':
            self.period = 'année'
            self.period_factor = 1
        else:
            raise ValueError("Période invalide")

    def build_hierarchy(self, df):
        hierarchy = {}
        unique_codes = df["Code de la catégorie"].unique()

        for code in unique_codes:
            parts = [p.strip() for p in code.split('>')]
            if len(parts) >= 4:
                categorie_principale = parts[2]
                sous_categorie = parts[3]
                if categorie_principale not in hierarchy:
                    hierarchy[categorie_principale] = []
                if sous_categorie not in hierarchy[categorie_principale]:
                    hierarchy[categorie_principale].append(sous_categorie)
        return hierarchy

    def select_category(self, dataset, cat_principale_index=None, sous_cat_index=None):
        """
        Cette fonction est adaptée pour être utilisée dans main.py qui gère l'input.
        Ici, on peut simplement fournir des méthodes pour obtenir les listes de catégories/sous-catégories
        et laisser main.py décider.
        """
        if dataset == 'equipements':
            return 'equipements', None
        # Si cat_principale_index et sous_cat_index sont fournis, on retourne directement la sous catégorie
        categories_principales = list(self.hierarchies[dataset].keys())
        if cat_principale_index is not None:
            cat_principale = categories_principales[cat_principale_index]
            sous_categories = self.hierarchies[dataset][cat_principale]
            if sous_cat_index is not None:
                return cat_principale, sous_categories[sous_cat_index]
            else:
                return cat_principale, None
        else:
            return None, None

    def get_main_categories(self, dataset):
        if dataset == 'equipements':
            return []
        return list(self.hierarchies[dataset].keys())

    def get_sub_categories(self, dataset, cat_principale):
        if dataset == 'equipements':
            return []
        return self.hierarchies[dataset][cat_principale]

    def search_product(self, dataset, query=None, categorie_principale=None, sous_categorie=None):
        if dataset == 'aliments':
            df = self.df_aliments
        elif dataset == 'energie':
            df = self.df_energie
        elif dataset == 'equipements':
            df = self.df_equipements

        if categorie_principale and sous_categorie:
            df = df[df["Code de la catégorie"].str.contains(categorie_principale, case=False, na=False) &
                    df["Code de la catégorie"].str.contains(sous_categorie, case=False, na=False)]

        if query:
            query = query.lower()
            df = df[df["Nom base français"].str.contains(query, na=False)]

        return df

    def add_consumption(self, dataset, product_id, quantite):
        if dataset == 'aliments':
            df = self.df_aliments
        elif dataset == 'energie':
            df = self.df_energie
        elif dataset == 'equipements':
            df = self.df_equipements

        line = df[df["Identifiant de l'élément"] == float(product_id)]
        if line.empty:
            print("Aucun produit trouvé avec cet ID.")
            return

        nom = line["Nom base français"].values[0]
        co2_unitaire = line["CO2"].values[0]
        unite = line["Unité français"].values[0]

        if dataset in ['aliments', 'energie']:
            quantite_annuelle = quantite * self.period_factor
        else:
            quantite_annuelle = quantite

        co2_total = co2_unitaire * quantite_annuelle

        self.consumptions.append({
            'type': dataset,
            'produit': nom,
            'quantite': quantite_annuelle,
            'unite': unite,
            'co2_unitaire': co2_unitaire,
            'co2_total': co2_total
        })
        print(f"Produit ajouté avec succès ! Emissions : {co2_total:.2f} kgCO2e/an")

    def show_total_emissions(self):
        if not self.consumptions:
            print("Aucune consommation enregistrée.")
            return
        total = sum(item['co2_total'] for item in self.consumptions)
        print(f"\nTotal des émissions annuelles de CO2e : {total:.2f} kgCO2e")

