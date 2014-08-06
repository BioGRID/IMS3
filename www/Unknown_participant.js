IMS.Unknown_participant=function(data){
  this.data=data;
}
IMS.Unknown_participant.prototype=new IMS._table();
IMS.Unknown_participant.prototype.html=function(){
  var org=this.data.organism_id;
  var id=this.data.unknown_participant_identifier;
  var clazz='o'+org;

  var html=IMS.cache(
    {table:IMS.constant(IMS.Quick_organism,'table'),
     organism_id:org},
    function(data){
      qo=new IMS.Quick_organism(data[0]);
      //console.log(qo);
      var html=qo.html();
      $('.'+clazz).replaceWith(html);
      return html;
    },'organism_id');
  $('.footnotes .asterisk').removeClass('hide');
  if(!html){
    html='<span class="'+clazz+'">'+org+'</span>';
  }
  return id+'* ('+html+')';
}