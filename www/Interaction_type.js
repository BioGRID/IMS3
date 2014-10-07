IMS.Interaction_type=function(data){
  this.data=data;
}

IMS.Interaction_type.prototype=new IMS._table();
IMS.Interaction_type.prototype._const={
  table:'interaction_types',
  primary_col:'interaction_type_id',
  html_class:'interaction_types'
}

/*
 * nonstatic
 */

IMS.Interaction_type.prototype.html=function(){
  return this.data.interaction_type_name;
}
