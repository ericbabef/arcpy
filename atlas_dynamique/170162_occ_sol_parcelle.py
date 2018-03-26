mxd = arcpy.mapping.MapDocument("CURRENT")
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum
	row = mxd.dataDrivenPages.pageRow
	pageName = mxd.dataDrivenPages.pageRow.id_par
	
	df = arcpy.mapping.ListDataFrames(mxd)[1]
	lyr = arcpy.mapping.ListLayers(mxd, 'occ_sol', df)[0]
	where_clause = "id_par = '" + pageName + "'"
	lyr.definitionQuery = where_clause
	df.extent = lyr.getSelectedExtent(False)
	df.scale = df.scale * 8
	
    print "Page {0} sur {1}".format(str(mxd.dataDrivenPages.currentPageID), str(mxd.dataDrivenPages.pageCount))
	ddp = mxd.dataDrivenPages
    ddp.exportToPDF(r"I:\CARTO\Cartes en images\Projets communautaires\Environnement et sport\cours_deau\occupation_parcelle\plan_" + str(pageNum) + ".pdf", "CURRENT")
del mxd