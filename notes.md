cas 1 = pas de correspondances
    code 1
    message : pas de correspondances

cas 2 = correspondances approximatives
    code 2
    message : Plusieurs équipements correspondent. Vouliez vous dire :
    json : liste des propositions

cas 3 = doublons
    code 3
    message : Plusieurs éléments avec le même nom, veuillez entrer l'ID de l'équipement :
    json : liste des IDs

cas 4 = correspondance complete
    code 4
    message : Equipement trouvé, que souhaitez vous savoir dessus?
    json : id de l'équipement