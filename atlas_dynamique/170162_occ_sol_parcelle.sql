select distinct
CAST (ROW_NUMBER() OVER (ORDER BY a.globalid ASC) as INTEGER) as id, 
a.globalid, a.commentaire,  
b.ripisylve as berge_ripisylve, b.densite as berge_densite, b.largeur as berge_largeur, b.strate1 as berge_strate1, b.strate2 as berge_strate2, b.strate3 as berge_strate3, 
d.commentaire as patri_commentaire,  
string_agg(DISTINCT e.type, ', ') as possi_type, string_agg(DISTINCT e.commentaire, ', ') as possi_commentaire,
f.type as eau_type, f.commentaire as eau_commentaire, 
string_agg(DISTINCT g.type_milieu, ', ') as milieu_type, string_agg(DISTINCT g.type_milieu_desc, ', ') as milieu_desc, 
string_agg(DISTINCT h.type_usage, ', ') as usage_type, string_agg(DISTINCT h.desc_usage, ', ') as usage_desc, 
('I:\\CARTO\Cartes en images\\Projets communautaires\\Environnement et sport\\cours_deau\\occupation_parcelle\image\\' || c.id_par || '.jpg') as image_path,
c.id_par, c.section, c.texte, c.geom  
from cahm.coursdeau_identification_parcelle a cross join cadastre.parcelle c  
left outer join cahm.coursdeau_berge b on (a.globalid = b.id)  
left outer join cahm.coursdeau_espece_patrimoniale d on (a.globalid = d.id)  
left outer join cahm.coursdeau_possibilite e on (a.globalid = e.id)  
left outer join cahm.coursdeau_type_eau f on (a.globalid = f.id)  
left outer join cahm.coursdeau_type_milieu g on (a.globalid = g.id)  
left outer join cahm.coursdeau_usage_activite h on (a.globalid = h.id)  
where st_intersects(c.geom, a.geom) 
group by c.id_par, a.globalid, a.commentaire, b.ripisylve, b.densite, b.largeur, b.strate1, b.strate2, b.strate3, f.type, f.commentaire, d.commentaire
order by c.id_par