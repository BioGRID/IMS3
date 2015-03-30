IMS.Interaction_ontology_qualifier=function(data){
  this.data=data;
}

// The PHP query for Interaction_ontology_qualifier joins the
// Ontology_term row, so when printing we want to use the same html()
// function.
IMS.Interaction_ontology_qualifier.prototype=new IMS.Ontology_term();
IMS.Interaction_ontology_qualifier.prototype._const={
  'table':'interaction_ontologies_qualifiers',
  'primary_col':'interaction_ontology_qualifier_id',
}
