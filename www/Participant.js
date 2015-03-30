IMS.Participant=function(data){
  this.data=data;
}
IMS.Participant.prototype=new IMS._table();
IMS.Participant.prototype._const={
  table:'participants',
  primary_col:'participant_id',
}

/*
 * static
 */

/*
IMS.Participant.prototype.ok=function(col,val,tag){
  if((this.primary_col()==col) && (val=='add')){
    tag.html('<button data-toggle="modal" data-target="#participant_selector">add</button>');
    return false;
  }
  return true;
}
*/

// Returns a value unique to this object, and suitable to be used in a
// HTML class attribute.
IMS.Participant.prototype.clazz=function(){
  return 'id'+this.data.participant_id+'type'+this.data.participant_type_id;
}

IMS.Participant.prototype.html=function(){
  var clazz=this.clazz();
  var that=this;

  switch(this.data.participant_type_id){
    case '0':
    IMS.query
    ({
      table:'unknown_participants',
      unknown_participant_id:this.data.participant_value},
     function(data){
       up=new IMS.Unknown_participant(data[0]);
       $('.'+clazz).html(up.html());
     });
    break;
    case '1':
    IMS.query
    ({
      table:'quick_identifiers',
      quick_identifier_type:'OFFICIAL SYMBOL',
      gene_id:this.data.participant_value},
     function(data){
       qi=new IMS.Quick_identifier(data[0]);
       $('.'+clazz).html(qi.html());
    });
  }
  return '<span class="'+clazz+'">'+clazz+'</span>';
}
