from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
#Création de FastAPI
app = FastAPI(title="API Facturation Okayo", version="1.0.0")

# ---- MODELES DE TABLES ----
class Client(BaseModel):
    id: Optional[int] = None
    code_client: str
    nom_client: str
    adresse: str
    ville: str
    code_postal: str
    pays: str
    telephone: Optional[str] = None
    email: Optional[str] = None

class Produit(BaseModel):
    id: Optional[int] = None
    code_produit: str
    nom: str
    description: Optional[str] = None
    prix_unitaire_ht: float

class LigneFacture(BaseModel):
    produit_id: int
    designation: str
    prix_unitaire_ht: float
    quantite: int
    tva_appliquee: float
    montant_ht: Optional[float] = None
    montant_ttc: Optional[float] = None

class Facture(BaseModel):
    id: Optional[int] = None
    reference: str
    client_id: int
    date_facturation: str
    date_echeance: str
    conditions_reglement: str
    lignes: List[LigneFacture]
    total_ht: Optional[float] = 0.0
    total_tva: Optional[float] = 0.0
    total_ttc: Optional[float] = 0.0

# ---- DATABASES SIMPLIFIÉES ----
clients_db: List[Client] = []
produits_db: List[Produit] = []
factures_db: List[Facture] = []

# ---- ROUTES CLIENTS ----
#ajouter un client
@app.post("/clients", response_model=Client)
def creer_client(client: Client):
    client.id = len(clients_db) + 1
    clients_db.append(client)
    return client

#afficher les informations de client
@app.get("/clients/{id}", response_model=Client)
def lire_client(id: int):
    for c in clients_db:
        if c.id == id:
            return c
    raise HTTPException(status_code=404, detail="Client non trouvé")

#afficher tous les clients
@app.get("/clients", response_model=List[Client])
def lister_clients():
    return clients_db

# ---- ROUTES PRODUITS ----
#ajouter un porduit
@app.post("/produits", response_model=Produit)
def creer_produit(produit: Produit):
    produit.id = len(produits_db) + 1
    produits_db.append(produit)
    return produit

#afficher les informations de produit 
@app.get("/produits/{id}", response_model=Produit)
def lire_produit(id: int):
    for p in produits_db:
        if p.id == id:
            return p
    raise HTTPException(status_code=404, detail="Produit non trouvé")

#afficher tous les produits
@app.get("/produits", response_model=List[Produit])
def lister_produits():
    return produits_db

# ---- ROUTES FACTURES ----
#créer une facture et calcul du prix
@app.post("/factures", response_model=Facture)
def creer_facture(facture: Facture):
    # Vérifier que le client existe
    client = next((c for c in clients_db if c.id == facture.client_id), None)
    if not client:
        raise HTTPException(status_code=400, detail="Client inexistant")

    total_ht = 0.0
    total_tva = 0.0
    total_ttc = 0.0

    lignes_calculees = []
    for ligne in facture.lignes:
        # Vérifier que le produit existe
        prod = next((p for p in produits_db if p.id == ligne.produit_id), None)
        if not prod:
            raise HTTPException(status_code=400, detail=f"Produit {ligne.produit_id} inexistant")

        # Calculs du prix
        montant_ht = ligne.prix_unitaire_ht * ligne.quantite
        montant_tva = montant_ht * (ligne.tva_appliquee / 100)
        montant_ttc = montant_ht + montant_tva

        total_ht += montant_ht
        total_tva += montant_tva
        total_ttc += montant_ttc

        # Construire la ligne complète avec calculs
        lignes_calculees.append(LigneFacture(
            produit_id=ligne.produit_id,
            designation=ligne.designation,
            prix_unitaire_ht=ligne.prix_unitaire_ht,
            quantite=ligne.quantite,
            tva_appliquee=ligne.tva_appliquee,
            montant_ht=montant_ht,
            montant_ttc=montant_ttc
        ))

    facture.id = len(factures_db) + 1
    facture.lignes = lignes_calculees
    facture.total_ht = round(total_ht, 2)
    facture.total_tva = round(total_tva, 2)
    facture.total_ttc = round(total_ttc, 2)

    factures_db.append(facture)
    return facture

#afficher les informations d'une facture 
@app.get("/factures/{facture_id}")
def lire_facture(facture_id: int):
    for facture in factures_db:
        if facture.id == facture_id:
            return facture
    raise HTTPException(status_code=404, detail="Facture non trouvée")

#afficher toutes les factures
@app.get("/factures")
def lister_factures():
    return factures_db