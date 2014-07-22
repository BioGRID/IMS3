IMS.Interaction_participant=function(data){
  this.data=data;
}

IMS.Interaction_participant.prototype=new IMS._table();
IMS.Interaction_participant.prototype._const={
  primary_key:'interaction_participant_id',

  table_id:'#participants',
  count_class:'.participant-count'
};
IMS.Interaction_participant.prototype.dts=function(){
  return [
    'interaction_participant_id',
    //'interaction_id',
    //'participant_id',
    'participant',
    //'participant_role_id',
    'participant_role',
    'interaction_participant_addeddate',
    'interaction_participant_status',
  ];
}
