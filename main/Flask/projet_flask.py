from flask import Flask, render_template, request, flash
import sqlite3

app = Flask(__name__)

app.secret_key = "d6f12217b2b3ee3a5f0cf986d0e74658217c0b7c63080a6bc39a0e4575b4534c" # Mot de Passe "CarnetContact" encodé en sha256

path_bdd = "ContactBDD.db"

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/confirmation", methods =["POST"])
def add_contact():
    mail = request.form['Mail']
    adresse = request.form['Adresse']
    téléphone = request.form['Téléphone']
    catégorie = request.form['Catégorie']
    prénom = request.form['Prénom']
    nom = request.form['Nom']
    
    error = [""" Une Erreur dans la saisie est détéctée. """]
    
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
        
    if len(error) > 1:
        return render_template("consultPage.html", titre="Erreur lors de l'enregistrement", Component="\n".join(error))
    else :
        conn = sqlite3.connect(path_bdd)
        cursor = conn.cursor()
        user = (nom, prénom, catégorie, téléphone, mail, adresse)

        cursor.execute("""
            INSERT INTO users (nom, prenom, catégorie, teléphone, mail, adresse)
            VALUES (?, ?, ?, ?, ?, ?)
        """, user)
        conn.commit()
        conn.close()
        return render_template("consultPage.html", titre="Enregistrement du Contact Réussi.", Component=f"Le Contact Suivant a bien été enregistré dans la Base de Données : {nom}  {prénom} {catégorie} '{téléphone}' {adresse}  {mail}")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == "__main__":
    app.run(debug=True)
