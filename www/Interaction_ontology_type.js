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

// To be more consistant with IMS2 display the shortcodes
IMS.Interaction_ontology_type.prototype.option_html=function(selected){
  var sc=this.data.interaction_ontology_type_shortcode;
  var sel='';
  if(selected && (selected==this.id)){
    sel=' SELECTED';
  }

  var out='<option class="iot_'.
    concat(sc,'"',sel,
           ' value="',this.primary_id(),
           '">[',sc,']</option>');
  return out;
}
