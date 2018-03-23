import arcpy, json, os, xml.etree.cElementTree as ET

arcpy.env.overwriteOutput = True

with open(r"maj_champs_dict_field.json") as config_file:
    dict_field = json.load(config_file)

try:
   for nom_commune, code_insee in dict_field.items():
       select_commune = arcpy.MakeFeatureLayer_management(os.environ['USERPROFILE'] + '\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\187_agglo_sig.sde\\agglo.sig.habillage_communes_agglo','commune_lyr')
       whereClause = "nom = '" + nom_commune + "'"
       arcpy.SelectLayerByAttribute_management(select_commune, "NEW_SELECTION", whereClause)
       print(nom_commune)

       tree = ET.ElementTree(file='maj_champs_xml_bdd.xml')
       for elem in tree.iter(tag='layer'):
           bdd = elem.get('bdd')
           name_layer = elem.get('name')
           field_nom_com = elem.findtext('nomcom')
           field_code_insee = elem.findtext('codeinsee')

           try:
               select_emplacement = arcpy.MakeFeatureLayer_management(os.environ['USERPROFILE'] + '\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\187_' + bdd +'_sig.sde\\' + name_layer, 'lyr')
               arcpy.SelectLayerByLocation_management(select_emplacement, 'INTERSECT', select_commune)

               fields = [field_nom_com, field_code_insee]
               with arcpy.da.UpdateCursor(select_emplacement, fields) as cursor:
                   for row in cursor:
                       row[0] = nom_commune
                       row[1] = code_insee
                       cursor.updateRow(row)

               #cnt = arcpy.GetCount_management(select_emplacement)
               #print "Nb maj : " + str(cnt)
           except:
               print(arcpy.GetMessages())

except:
   print(arcpy.GetMessages())