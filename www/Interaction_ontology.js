IMS.Interaction_ontology=function(data){
  this.data=data;
}

IMS.Interaction_ontology.prototype=new IMS._table();
IMS.Interaction_ontology.prototype._const={
  table:'interaction_ontologies',
  primary_col:'interaction_ontology_id',
  html_class:'ontologies'
};

IMS.Interaction_ontology.prototype.dts=function(){
  return [
    //'interaction_ontology_id',
    //'interaction_id',
    //'ontology_term_id',
    'ontology_term',
    //'user_id',
    'user',
    'interaction_ontology_type_id',
    //'interaction_ontology_addeddate',
    'interaction_ontology_status',
  ];
};
