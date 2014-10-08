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


IMS.Participant.prototype.ok=function(col,val,tag){
  if((this.primary_col()==col) && (val=='add')){
    console.log(col,val);
    tag.html('<button data-toggle="modal" data-target="#participant_selector">add</button>');

    return false;
  }
  return true;
}


IMS.Participant.prototype.html=function(){
  var clazz='id'+this.data.participant_id+'type'+this.data.participant_type_id;
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


/*

$(document).ready(function(){
  // prep the HTML in home.php to select a participant

  console.log('yup, got it');
});

*/
