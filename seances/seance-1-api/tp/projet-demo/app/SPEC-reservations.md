
Remplissez ce tableau dans un fichier `REVIEW.md` :

| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Les codes de statut correspondent à la spec (201, 404, 409) |ok | |
| `response_model` présent sur les 4 routes |ok| j'ai ajouté le `response_model` sur toutes les routes |
| La validation `date_fin > date_debut` est bien dans le schéma Pydantic |ok | |
| Le router n'accède pas au stockage de `items` |ok | |
| Pas d'`async def` sans `await` |?| |
| Aucune dépendance ajoutée dans `requirements.txt` (ou justifiée) | ok| |
| Les routes littérales sont déclarées avant les routes paramétrées |oui | |
| Le code renvoie une réponse cohérente pour `POST /reservations/999/annuler` oui| | |