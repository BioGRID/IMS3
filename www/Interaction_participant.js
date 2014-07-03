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
IMS.Interaction_participant.prototype.dd=function(dt){
  switch(dt){
    case 'participant_role':
    return this.cache(dt).html();
    case 'participant':
    return this.cache(dt,sessionStorage).html();
  }
  return this.data[dt];
}
