IMS.Interaction_participant=function(data){
  this.data=data;
}

IMS.Interaction_participant.prototype=new IMS._table();
IMS.Interaction_participant.prototype._const={
  table:'interaction_participants',
  primary_col:'interaction_participant_id',
  html_id:'participants',
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
