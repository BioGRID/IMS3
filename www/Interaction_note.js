IMS.Interaction_note=function(data){
  this.data=data;
}

IMS.Interaction_note.prototype=new IMS._table();
IMS.Interaction_note.prototype._const={
  table:'interaction_notes',
  primary_col:'interaction_note_id',
}

IMS.Interaction_note.prototype.html=function(){
  return this.data.interaction_note_text;
}