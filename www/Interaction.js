IMS.Interaction=function(data){
  this.data=data;
  this.new_id=0;

  this.participants={};  // list of participants (er, Interaction_participants)
  this.participant=null; // selected participant (ibid.)
}

IMS.Interaction.prototype=new IMS._table();
IMS.Interaction.prototype._const={
  table:'interaction',
  primary_col:'interaction_id',
  html_class:'interactions'
};

/*
 * static
 */

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


// types should be loaded at startup, so I'm not worried about them
// not being there.
IMS.Interaction.prototype.type=function(){
  return IMS.getItem(IMS.Interaction_type,this.data.interaction_type_id);
}