# -*- coding: UTF8 -*-
import arcpy, json, re, os

def path_mxd(path_mxd):
    path_mxd = path_mxd
    return reparation_mxd(path_mxd)

def reparation_mxd(path_mxd):
    mxd = arcpy.mapping.MapDocument(path_mxd)

    # list BDD
    list_bdd = ['agglo']
    for list_bdd in list_bdd:

        oldpath = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\35_" + list_bdd + "_sig.sde"
        print oldpath
        newpath = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\187_" + list_bdd + "_sig.sde"
        print newpath
        #mxd = arcpy.mapping.MapDocument(r"C:/Users/e.babef/Documents/test_mxd/maj_mxd.mxd")
        # changer le nom du serveur
        mxd.findAndReplaceWorkspacePaths(
            oldpath,
            newpath,
            False)
    mxd.save()

    #accès aux nom des jeux de classe + préfixes
    jeu_de_classe = {}
    with open(r"C:/Users/e.babef/Documents/test_mxd/jeu_de_classe.json") as config_file:
        jeu_de_classe = json.load(config_file)

    #parcours les couches rompues
    for lyr in arcpy.mapping.ListBrokenDataSources(mxd):
        try:
            #chemin de la donnée
            source_data =  lyr.dataSource
            source_data = source_data
            print source_data

            #parcours les jeux de classe
            for dataset, dataset_pref in jeu_de_classe.items():
                try:
                    #nom du préfixe
                    name_pref = '{}'.format(dataset_pref)
                    #nom du jeu de classe
                    name_jeu_de_classe = '{}'.format(dataset)
                    print name_jeu_de_classe

                    #expression pour rechercher le nom du jeu de classe dans le chemin de la donnée
                    data_expression = re.findall((name_jeu_de_classe), source_data)
                    print data_expression
                    #expression pour rechercher le nom de la couche
                    #nom_couche = re.findall(r"[a-zA-Z0-9_]+$", source_data)
                    nom_couche = os.path.split(source_data)
                    nom_couche = re.findall(r"[a-zA-Z0-9_]+$", nom_couche[1])
                    nom_couche = nom_couche[0].lower()

                    #test si expression retourne un résultat
                    if len(data_expression) == 1:

                        #création du nouveau nom de couche
                        new_nm = "agglo.sig." + name_pref + "_" + nom_couche
                        print new_nm

                        lyr.replaceDataSource(r"C:\Users\e.babef\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\187_agglo_sig.sde", "NONE", new_nm)
                    else:
                        print 'erreur'
                except Exception:
                    print 'erreur'
        except Exception:
            print 'erreur'

    mxd.save()
    del mxd

if __name__ == '__main__':
    path_mxd(r"C:/Users/e.babef/Documents/test_mxd/maj_mxd.mxd",)