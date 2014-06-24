IMS.Interaction_type=function(data){
  this.data=data;
}
IMS.Interaction_type.prototype=new IMS._table();
IMS.Interaction_type.prototype._table='interaction_types';
IMS.Interaction_type.prototype._cols={
  primary_key:'interaction_type_id'
}
IMS.Interaction_type.prototype.html=function(){
  return this.data.interaction_type_name;
}