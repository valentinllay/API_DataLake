def say_hello_world():
 """
 Renvoie le texte de salutation.
 """
 return "Hello world !"


def personalized_greeting(genre=None, prenom=None, nom=None):
    """
    Renvoie une salutation personnalisée selon le genre, prénom et nom.
    """
    # Cas complet
    if genre and prenom and nom:
        return f"Bonjour {genre} {prenom} {nom}."
    # Prénom et nom uniquement
    if prenom and nom:
        return f"Bonjour {prenom} {nom}."
    # Prénom uniquement
    if prenom:
        return f"Bonjour {prenom}."
    # Message générique
    return "Bonjour."
