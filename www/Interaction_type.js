IMS.Interaction_type=function(data){
  this.data=data;
}

/*
 * Prototype
 */

IMS.Interaction_type.prototype=new IMS._table();
IMS.Interaction_type.prototype._const={
  table:'interaction_types',
  primary_col:'interaction_type_id',
}
IMS.Interaction_type.prototype.html=function(){
  return this.data.interaction_type_name;
}