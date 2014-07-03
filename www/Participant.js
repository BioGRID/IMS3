IMS.Participant=function(data){
  this.data=data;
}
IMS.Participant.prototype=new IMS._table();
IMS.Participant.prototype._const={
  table:'participants',
  primary_key:'participant_id',
}
IMS.Participant.prototype.html=function(){
  return '<span class="text-danger">'
       +this.data.participant_id+'&#9888;'+this.data.participant_type_id
       +'</span>';
}