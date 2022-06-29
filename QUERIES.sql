select * from protein
where length>500;

select * from locus
where exon_count>10;

select i.protein_id, i.isoform_num, i.length
from isoform i JOIN protein p ON i.protein_id=p.id
where p.length>500;

select g.name, l.map_location
from gene g JOIN locus l ON g.id=l.gene
where map_location IS NOT NULL;

select * from isoform
where length < (select min(length) from protein);

select * from locus
where gene IN (select id from gene
where organism = (select tax_id from organism
where name = 'Homo sapiens'));