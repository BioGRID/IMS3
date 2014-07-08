IMS.Participant=function(data){
  this.data=data;
}
IMS.Participant.prototype=new IMS._table();
IMS.Participant.prototype._const={
  table:'participants',
  primary_key:'participant_id',
}
IMS.Participant.prototype.html=function(){
  var clazz='id'+this.data.participant_id+'type'+this.data.participant_type_id;
  var that=this;
  switch(this.data.participant_type_id){
    case '1':
    // This is current not being cached, gotta fix that.
    $.ajax({
      async:true,
      type:'GET',
      url:'query.php',
      dataType:'json',
      data:{
        table:'quick_identifiers',
        quick_identifier_type:'OFFICIAL SYMBOL',
        gene_id:this.data.participant_value,
      }
    }).done(function(data){
      IMS.report_messages(data.messages);
      qi=new IMS.Quick_identifiers(data.results[0]);
      $('.'+clazz).html(qi.html());
      //console.log(that.data.participant_value);
    });
  }
  return '<span class="'+clazz+'">'+clazz+'</span>';
}
