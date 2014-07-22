IMS.Interaction=function(data){
  this.data=data;
  IMS.Interaction._interactions[this.id]=this;
}

IMS.Interaction.prototype=new IMS._table();
IMS.Interaction.prototype._const={
  table:'interaction',
  primary_key:'interaction_id',

  // how to access elements in the DOM
  table_id:'#interactions',
  count_class:'.interaction-count'
};
IMS.Interaction.prototype.dts=function(){
  return [
    'interaction_id',
    //'participant_hash',
    //'publication_id',
    //'interaction_type_id',
    'interaction_type',
    'interaction_status',
    //'interaction_source_id',
    'interaction_source',
    'state',
  ];
}
