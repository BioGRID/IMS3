IMS.Interaction=function(data){
  this.data=data;
}

IMS.Interaction.prototype=new IMS._table();
IMS.Interaction.prototype._cols={
  primary_key:'interaction_id'
};
IMS.Interaction.prototype.dts=function(){
  return [
    'interaction_id',
    //'participant_hash',
    'publication_id',
    //'interaction_type_id',
    'interaction_type',
    'interaction_status',
    //'interaction_source_id',
    'interaction_source',
  ];
}
IMS.Interaction.prototype.dd=function(dt){
  switch(dt){
    case 'interaction_source':
    case 'interaction_type':
    return this.cache(dt).html();
  }
  return this.data[dt];
}
