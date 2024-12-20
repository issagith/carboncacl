import pandas as pd
from carboncalc.calculator import CarbonCalculator
from carboncalc.results import generate_report

if __name__ == "__main__":
    # Charger les données
    df_aliments = pd.read_csv("data/aliments_extrait.csv", sep=",", quotechar='"')
    df_energie = pd.read_csv("data/energie_extrait.csv", sep=",", quotechar='"')
    df_equipements = pd.read_csv("data/equipements_extrait.csv", sep=",", quotechar='"')

    calc = CarbonCalculator(df_aliments, df_energie, df_equipements)

    print("Bienvenue dans le calculateur d'empreinte carbone !")
    print("Sur quelle période souhaitez-vous entrer vos quantités ?")
    print("1. Jour")
    print("2. Semaine")
    print("3. Mois")
    print("4. Année")
    while True:
        choix = input("Entrez le numéro correspondant : ").strip()
        if choix == '1':
            calc.set_period('jour')
            break
        elif choix == '2':
            calc.set_period('semaine')
            break
        elif choix == '3':
            calc.set_period('mois')
            break
        elif choix == '4':
            calc.set_period('année')
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

    while True:
        print("\nChoisissez un poste de consommation :")
        print("1. Aliments")
        print("2. Energie")
        print("3. Equipements")
        print("4. Fin")

        choice = input("Entrez le numéro correspondant à votre choix : ").strip()

        if choice == '4':
            calc.show_total_emissions()
            print("Voulez-vous générer un rapport ? (o/n)")
            rep = input().strip().lower()
            if rep == 'o':
                generate_report(calc.consumptions, "report.html")
            print("Merci d'avoir utilisé le calculateur d'empreinte carbone !")
            break
        elif choice == '1':
            dataset_choice = 'aliments'
        elif choice == '2':
            dataset_choice = 'energie'
        elif choice == '3':
            dataset_choice = 'equipements'
        else:
            print("Choix invalide. Veuillez réessayer.")
            continue

        if dataset_choice == 'equipements':
            # Pas de catégories, on passe directement à la boucle query
            cat_principale, sous_cat = 'equipements', None
        else:
            # Sélection de la catégorie principale
            main_cats = calc.get_main_categories(dataset_choice)
            if not main_cats:
                cat_principale, sous_cat = 'equipements', None
            else:
                # Choix de la catégorie
                while True:
                    print("\nNavigation par catégories :")
                    for i, c in enumerate(main_cats):
                        print(f"{i+1}. {c}")
                    choix_cat = input("Choisissez une catégorie principale (numéro) ou 'back' : ").strip()
                    if choix_cat.lower() == 'back':
                        cat_principale, sous_cat = None, None
                        break
                    try:
                        ci = int(choix_cat)-1
                        if ci < 0 or ci >= len(main_cats):
                            print("Choix invalide")
                            continue
                        cat_principale = main_cats[ci]
                        # Choix de la sous catégorie
                        sub_cats = calc.get_sub_categories(dataset_choice, cat_principale)
                        while True:
                            print("\nSous-catégories disponibles :")
                            for i, sc in enumerate(sub_cats):
                                print(f"{i+1}. {sc}")
                            choix_sc = input("Choisissez une sous-catégorie (numéro) ou 'back' : ").strip()
                            if choix_sc.lower() == 'back':
                                # Retour au choix catégorie principale
                                cat_principale, sous_cat = None, None
                                break
                            try:
                                sci = int(choix_sc)-1
                                if sci < 0 or sci >= len(sub_cats):
                                    print("Choix invalide.")
                                    continue
                                sous_cat = sub_cats[sci]
                                break
                            except ValueError:
                                print("Saisie invalide.")
                        if sous_cat is not None:
                            break
                    except ValueError:
                        print("Saisie invalide.")
                if cat_principale is None and sous_cat is None:
                    # back au menu principal
                    continue

        # Boucle pour saisie du query
        while True:
            if dataset_choice == 'equipements':
                query = input("Mot-clé équipements ou appuyer sur Entrer pour afficher les produits (ou 'back') : ").strip()
                if query.lower() == 'back':
                    break
                results = calc.search_product(dataset_choice, query=query)
            else:
                query = input(f"Mot-clé dans {sous_cat} ou appuyer sur Entrer pour afficher les produits (ou 'back') : ").strip()
                if query.lower() == 'back':
                    # On retourne à la sélection de la catégorie
                    # (pour simplifier, on quitte cette boucle => retour menu principal)
                    break
                results = calc.search_product(dataset_choice, query=query, categorie_principale=cat_principale, sous_categorie=sous_cat)

            if results.empty:
                print("Aucun produit trouvé.")
                continue
            else:
                display_results = results[["Identifiant de l'élément", "Nom base français", "CO2", "Unité français"]]
                print("\nProduits trouvés :")
                for idx, row in display_results.iterrows():
                    line_number = display_results.index.get_loc(idx) + 1
                    print(f"{line_number}. {row['Nom base français']} - CO2: {row['CO2']} {row['Unité français']}")

                # Choix du produit
                while True:
                    id_choisi = input("Numéro du produit (ou 'back') : ").strip()
                    if id_choisi.lower() == 'back':
                        # retour au query
                        break
                    try:
                        line_choice = int(id_choisi) - 1
                        if line_choice < 0 or line_choice >= len(display_results):
                            print("Numéro de ligne invalide.")
                            continue
                    except ValueError:
                        print("Saisie invalide.")
                        continue

                    selected_product = display_results.iloc[line_choice]
                    product_id = selected_product["Identifiant de l'élément"]

                    if dataset_choice == 'aliments':
                        print(f"Entrez la quantité consommée par {calc.period} (ex: kg/{calc.period}) :")
                    elif dataset_choice == 'energie':
                        print(f"Entrez la quantité d'énergie consommée par {calc.period} (ex: kWh/{calc.period}) :")
                    elif dataset_choice == 'equipements':
                        print("Entrez le nombre d'unités achetées par an :")

                    try:
                        quantite = float(input("Quantité : "))
                        calc.add_consumption(dataset_choice, product_id, quantite)
                    except ValueError:
                        print("Quantité invalide, réessayez.")
