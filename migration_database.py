# -*- coding: UTF8 -*-
import arcpy, json, logging, re
from arcpy import env
from logging.handlers import RotatingFileHandler

def convert(old_path, new_path, json_file):
    "Fonction pour exporter des données stockées dans un jeu de classe. La nouvelle entité est préfixée à partir d'un dictionnaire"

    # création de l'objet logger qui va nous servir à écrire dans les logs
    logger = logging.getLogger()
    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 100Mo
    file_handler = RotatingFileHandler('activity.log', 'a', 100000000, 1)
    # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
    # créé précédement et on ajoute ce handler au logger
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # création d'un second handler qui va rediriger chaque écriture de log
    # sur la console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    #dictionnaire pour jeu de classe
    jeu_de_classe = {}
    with open(json_file) as config_file:
        jeu_de_classe = json.load(config_file)

    #boucle sur dictionnaire
    count = 0
    for dataset, dataset_pref in jeu_de_classe.items():
        try:
            env.workspace = old_path + "/{}".format(dataset)
            out_gdb = new_path

            #variable pour prefixe
            name_pref = '{}'.format(dataset_pref)
            name_jeu_de_classe = '{}'.format(dataset)

            logger.info('Jeu de classe : %s', name_jeu_de_classe)

            #variable pour liste data dans dataset
            fc_list = arcpy.ListFeatureClasses()

            #boucle sur data avec copy et rename
            for data in fc_list:
                try:
                    old_nm = data

                    data_expression = re.findall(r"[a-zA-Z0-9_]+$", old_nm)
                    data_expression = data_expression[0]

                    new_nm = name_pref + "_" + data_expression.lower()
                    nb_caract_data = 64
                    if len(new_nm) < nb_caract_data:
                        count = count + 1
                        arcpy.FeatureClassToFeatureClass_conversion(old_nm, out_gdb,new_nm)
                        #arcpy.CopyFeatures_management(oldnm, os.path.join(outgdb, newnm))
                        logger.info('%s est devenu %s', old_nm, new_nm)
                    else:
                        logger.warning('Trop de caracteres pour %s - jeu de classe %s', old_nm, name_jeu_de_classe)
                        continue
                except Exception:
                    logger.warning('Erreur sur %s - jeu de classe %s', old_nm, name_jeu_de_classe)
        except Exception:
            logger.warning('Erreur sur le jeu de classe %s', name_jeu_de_classe)
    logger.info('Données copiées : %s', count)
    logger.info('Traitements ok')