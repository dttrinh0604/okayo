run "pip install -r requirements.txt" to install fastapi and uvicorn

run "uvicorn main:app --reload" to start FastAPI application

go to "http://127.0.0.1:8000/docs" to see all of APIs


Fonctionnalités actuelles de l’API

1. Clients


Créer un client → POST /clients

Lire un client et ses informations → GET /clients/{id}

Lister tous les clients → GET /clients

    Exemple JSON (POST /clients) :
    
{
  "code_client": "CU2203-0005",
  
  "nom_client": "Mon Client SAS",
  
  "adresse": "45 rue du test",
  
  "ville": "Paris",
  
  "code_postal": "75016",
  
  "pays": "France",
  
  "telephone": "0102030405",
  
  "email": "client@test.fr"
  
}

3. Produits
Créer un produit → POST /produits
Lire un produit et ses informations → GET /produits/{id}
Lister tous les produits → GET /produits
    Exemple JSON (POST /produits) :
{
  "code_produit": "A",
  "nom": "Mon produit A",
  "description": "Service test",
  "prix_unitaire_ht": 1500.00
}

4. Factures
Créer une facture → POST /factures
⚠️ Il faut que client_id et produit_id existent.
Les montants (montant_ht, montant_ttc, total_ht, total_tva, total_ttc) sont calculés automatiquement.
Lister toutes les factures → GET /factures
Lire une facture spécifique → GET /factures/{id}

    Exemple JSON (POST /factures) :
{
  "reference": "2022-0025",
  "client_id": 1,
  "date_facturation": "2025-09-02",
  "date_echeance": "2025-09-10",
  "conditions_reglement": "Règlement à la livraison",
  "lignes": [
    {
      "produit_id": 1,
      "designation": "Mon produit A",
      "prix_unitaire_ht": 1500.00,
      "quantite": 2,
      "tva_appliquee": 5.5
    }
  ]
}
    Exemple réponse calculée automatiquement :
{
  "id": 1,
  "reference": "2022-0025",
  "client_id": 1,
  "date_facturation": "2025-09-02",
  "date_echeance": "2025-09-10",
  "conditions_reglement": "Règlement à la livraison",
  "lignes": [
    {
      "produit_id": 1,
      "designation": "Mon produit A",
      "prix_unitaire_ht": 1500.0,
      "quantite": 2,
      "tva_appliquee": 5.5,
      "montant_ht": 3000.0,
      "montant_ttc": 3165.0
    }
  ],
  "total_ht": 3000.0,
  "total_tva": 165.0,
  "total_ttc": 3165.0
}

