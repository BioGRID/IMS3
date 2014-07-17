IMS.Interaction_history=function(data){
  this.data=data;
}

IMS.Interaction_history.prototype=new IMS._table();
IMS.Interaction_history.prototype._const={
  primary_key:'interaction_history_id',
};
IMS.Interaction_history.prototype.modification_type=function(){
  return this.data.modification_type;
}
