IMS.Interaction_ontology_type=function(data){
  this.data=data;
}
IMS.Interaction_ontology_type.prototype=new IMS._table();
IMS.Interaction_ontology_type.prototype._const={
  table:'interaction_ontology_types',
  primary_col:'interaction_ontology_type_id',
  html_class:'interaction_ontology_types'
}

IMS.Interaction_ontology_type.prototype.html=function(){
  return this.data.interaction_ontology_type_name;
}