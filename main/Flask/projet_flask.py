# Import des bibliothèques nécessaires
from flask import Flask, render_template, request, flash
import sqlite3

# Initialisation de l'application Flask
app = Flask(__name__)

# Clé secrète utilisée pour la session
app.secret_key = "d6f12217b2b3ee3a5f0cf986d0e74658217c0b7c63080a6bc39a0e4575b4534c"  # Mot de Passe "CarnetContact" encodé en sha256

# Chemin de la base de données SQLite
path_bdd = "ContactBDD.db"

# Route principale pour la page d'accueil
@app.route("/")
def main():
    return render_template('main.html')


@app.route("/confirmation", methods=["POST"])
def add_contact():
    # Récupération des données du formulaire
    mail = request.form['Mail']
    adresse = request.form['Adresse']
    téléphone = request.form['Téléphone']
    catégorie = request.form['Catégorie']
    prénom = request.form['Prénom']
    nom = request.form['Nom']

    # Initialisation d'une liste d'erreur
    error = [""" Une Erreur dans la saisie est détéctée. """]

    # Validation des données du formulaire et construction de la liste d'erreur le cas échéant
    if mail == "" or (len(mail.split("@")) != 2 and len(mail.split(".") != 2)):
        error.append(f"Le Mail n'est pas conforme '{mail}'. (Ex: carnetContact@gmail.com) ")
    if adresse == "":
        error.append(f"L'adresse est vide . '{adresse}' ")
    if téléphone == "":
        error.append(f"Le Numéro de Téléphone est vide '{téléphone}'. Ex: +689 89 89 89 89")
    if catégorie == "":
        error.append(f"La Catégorie est vide '{catégorie}'. Ex: Famille, Amis")
    if prénom == "":
        error.append(f"Le Prénom est vide '{prénom}'. Ex: Jérôme")
    if nom == "":
        error.append(f"Le Nom est vide '{nom}'. Ex: De la Proutière")

    # Vérification de la présence d'erreurs
    if len(error) > 1:
        # Renvoi d'une page de consultation avec les erreurs
        return render_template("consultPage.html", titre="Erreur lors de l'enregistrement", Component="\n".join(error), path="http://localhost:5000/")
    else:
        # Connexion à la base de données SQLite et tentative d'insertion du contact
        conn = sqlite3.connect(path_bdd)
        cursor = conn.cursor()
        user = (nom, prénom, catégorie, téléphone, mail, adresse)

        cursor.execute("""
            INSERT INTO users (nom, prenom, catégorie, teléphone, mail, adresse)
            SELECT ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM users WHERE nom = ? AND prenom = ?
            )
        """, (*user, user[0], user[1]))
        # Vérifier le nombre de lignes affectées par l'opération d'insertion
        rows_affected = cursor.rowcount

        # Enregistrement des modifications dans la base de données
        conn.commit()
        conn.close()

        # Vérification de l'insertion et renvoi de réponses appropriées
        if rows_affected > 0:
            return render_template("consultPage.html", titre="Enregistrement du Contact Réussi.",
                                   Component=f"Le Contact Suivant a bien été enregistré dans la Base de Données : {nom}  {prénom} {catégorie} '{téléphone}' {adresse}  {mail}", path="http://localhost:5000/")
        else:
            return render_template("consultPage.html", titre="Erreur dans l'Enregistrement du Contact.",
                                   Component=f"Le Contact n'a pas été enregistré dans la base de données car il existe déjà", path="http://localhost:5000/")




@app.route("/consult")
def recherche():
    return render_template("consult.html")


@app.route("/consultPage", methods=["POST"])
def resultat():
    catégorie = request.form['Catégorie']
    text = request.form["Chercher"]

    conn = sqlite3.connect(path_bdd)
    cursor = conn.cursor()

    active = []

    visu_moyen = ""

    if catégorie == "*":
        active = cursor.execute("SELECT * FROM users").fetchall()
    if catégorie in ["famille", "travail", "amis"]:
        active = cursor.execute("SELECT * FROM users WHERE catégorie = ?", (catégorie,)).fetchall()
        visu_moyen = "par Catégorie"
    if catégorie == "nom":
        active = cursor.execute("SELECT * FROM users WHERE nom = ?", (text,)).fetchall()
        visu_moyen = "par Nom"
    if catégorie == "lettre":
        active = cursor.execute("SELECT * FROM users WHERE nom LIKE ?", (f"{text[0]}%",)).fetchall()
        visu_moyen = "par Lettre"

    conn.commit()
    conn.close()

    if active != []:
        activate = ["Nom Prénom Catégorie Téléphone Mail Adresse"]
        for x in active:
            myList = ""
            for index, y in enumerate(x):
                if index != 0:
                    myList = myList + f" {y}"
            activate.append(myList)
        print(activate)
        return render_template("consultPage.html", titre=f"Visualisation des Contacts {visu_moyen}", contacts=activate, path="http://localhost:5000/consult")
    else:
        return render_template("consultPage.html", titre="Erreur", Component=f"Le(s) Contact(s) suivant(s) n'existe(nt) pas. Ou la BDD est vide", path="http://localhost:5000/consult")


@app.route("/suppress")
def supp():
    return render_template("suppress.html")


@app.route("/suppression", methods=["POST"])
def suppression():
    nom = request.form['Nom']

    conn = sqlite3.connect(path_bdd)
    cursor = conn.cursor()
    cursor.execute("DELETE from users WHERE nom = ?", (nom, ))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    if rows_affected > 0:
        return render_template("consultPage.html", titre="Suppression d'un Contact par Nom",
                               Component=f"Le Contact {nom} a bien été supprimé de la BDD",
                               path="http://localhost:5000/suppress")
    else:
        return render_template("consultPage.html", titre="Erreur dans la Suppression du Contact",
                               Component=f"Le Contact {nom} n'existe pas",
                               path="http://localhost:5000/suppress")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
