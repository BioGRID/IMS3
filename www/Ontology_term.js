IMS.Ontology_term=function(data){
  this.data=data;
}

IMS.Ontology_term.prototype=new IMS._table();
IMS.Ontology_term.prototype._const={
  table:'ontology_terms',
  primary_col:'ontology_term_id',
}

IMS.Ontology_term.prototype.html=function(){
  var name=this.data.ontology_term_name;
  var desc=this.data.ontology_term_desc;
  var otoi=this.data.ontology_term_official_id;

  if(desc){
    desc=otoi + ': ' + desc;
  }else{
    desc=otoi;
  }

  return '<span data-toggle="tooltip" title="' + desc + '">' + name + '</span>';
}
