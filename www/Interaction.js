IMS.Interaction=function(data){
  this.data=data;
  this.new_id=0;
  this.participants=[];
}

IMS.Interaction.prototype=new IMS._table();
IMS.Interaction.prototype._const={
  html_id:'interactions',
  table:'interaction',
  primary_col:'interaction_id',
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
    'modification_type',
  ];
};

