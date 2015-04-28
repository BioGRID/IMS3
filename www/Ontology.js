IMS.Ontology=function(data){
  this.data=data;
}

IMS.Ontology.prototype=new IMS._table();
IMS.Ontology.prototype._const={
  table:'ontologies',
  primary_col:'ontology_id',
  html_class:'ontologies'
}

IMS.Ontology.prototype.html=function(){
  return this.data.ontology_name;
}