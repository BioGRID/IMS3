IMS.Interaction_source=function(data){
  this.data=data;
};
IMS.Interaction_source.prototype=new IMS._table();
IMS.Interaction_source.prototype._table='interaction_sources';
IMS.Interaction_source.prototype._cols={
  primary_key:'interaction_source_id'
}
IMS.Interaction_source.prototype.html=function(){
  url=this.data.interaction_source_url;
  name=this.data.interaction_source_name;

  if(url){
    return '<a href="'+url+'">'+name+'</a>';
  }
  return name;
}