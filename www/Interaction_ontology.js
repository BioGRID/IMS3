IMS.Interaction_ontology=function(data){
  this.data=data;
}

IMS.Interaction_ontology.prototype=new IMS._table();
IMS.Interaction_ontology.prototype._const={
  table:'interaction_ontologies',
  primary_col:'interaction_ontology_id',
  html_class:'ontologies'
};


/*
IMS.Interaction_ontology.prototype.dd=function(dt){
  vour out=IMS._table.prototype.dd.call(this,dt);
  if('qualifiers'==dt){

  }
  return out;
};
*/


IMS.Interaction_ontology.prototype.dts=function(){
  return [
    //'interaction_ontology_id',
    //'interaction_id',
    //'user_id',
    'user',
    //'interaction_ontology_type_id',
    'interaction_ontology_type',
    //'ontology_term_id',
    'ontology_term',
    'interaction_ontology_qualifier',
    //'interaction_ontology_addeddate',
    'interaction_ontology_status',
  ];
};
