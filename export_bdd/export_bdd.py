# -*- coding: UTF8 -*-
import arcpy, os
from arcpy import env

env.workspace = os.environ['USERPROFILE'] + "/AppData/Roaming/ESRI/Desktop10.5/ArcCatalog/agglo.sde/"
outgdb = "L:/_migration_database/agglo_backup_2018.gdb"

datasets = arcpy.ListDatasets("*", "Feature")

for dataset in datasets:
    dataset_create = dataset[10:]
    sr = arcpy.SpatialReference("lambert.prj")
    arcpy.CreateFeatureDataset_management(outgdb, dataset_create, sr)
    print '\nJeu de classe créé : ',dataset_create
    fcList = arcpy.ListFeatureClasses('', '', dataset)
    for shapefile in fcList:
        try:
            oldnm = shapefile
            newnm = shapefile[10:]
            arcpy.FeatureClassToFeatureClass_conversion(oldnm, outgdb + "/" + dataset_create, newnm)
            #arcpy.CopyFeatures_management(oldnm, os.path.join(outgdb + "/" + dataset_create, newnm))
            print 'données copiées : ',dataset_create,'/',newnm
        except Exception:
            print 'erreur : ', dataset_create, 'classe : ', newnm