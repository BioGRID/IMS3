IMS.Participant_role=function(data){
  this.data=data;
}
IMS.Participant_role.prototype=new IMS._table();
IMS.Participant_role.prototype._const={
  table:'participant_roles',
  primary_col:'participant_role_id',
  html_id:'participant_role'
}
IMS.Participant_role.prototype.html=function(){
  return this.data.participant_role_name;
}