IMS.Interaction=function(data){
  this.data=data;
}

IMS.Interaction.prototype=new IMS._table();
IMS.Interaction.prototype._const={
  table:'interaction',
  primary_key:'interaction_id',

  // how to access elements in the DOM
  table_id:'#interactions',
  count_class:'.interaction-count'
};
IMS.Interaction.prototype.dts=function(){
  return [
    'interaction_id',
    //'participant_hash',
    //'publication_id',
    //'interaction_type_id',
    'interaction_type',
    'interaction_status',
    //'interaction_source_id',
    'interaction_source',
    'state',
  ];
}
IMS.Interaction.prototype.dd=function(dt){
  switch(dt){
    case 'interaction_source':
    case 'interaction_type':
    return this.cache(dt).html();
    case 'state':
    return this.modification_type();
  }
  return this.data[dt];
}

IMS.Interaction.prototype.modification_type=function(){
  if(this.history){
    return this.history[0].modification_type();
  }
  var clazz=this.unique_html();
  var that=this;
  IMS.query(
    {table:'interaction_history',interaction_id:this.id},
    function(results){
      history=[];
      for(var row in results){
        history.push(new IMS.Interaction_history(results[row]));
      }
      $('.'+clazz).replaceWith(history[0].modification_type());
      that.history=history;
    });
  return '<span class="bg-danger '+clazz+'">unknown<span>';
}
