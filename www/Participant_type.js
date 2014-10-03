IMS.Participant_type=function(data){
  this.data=data;
}
IMS.Participant_type.prototype=new IMS._table();
IMS.Participant_type.prototype._const={
  table:'participant_types',
  primayr_col:'participant_type_id',
  html_id:'quick_type'
}
IMS.Participant_type.prototype.html=function(){
  return this.data.participant_type_name;
}