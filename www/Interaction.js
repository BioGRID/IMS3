IMS.Interaction=function(data){
  this.data=data;
  IMS.Interaction._active[this.id]=this;
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
};

IMS.Interaction.prototype.prop=function(prop,tag){
  if('state'==prop){
    if(this.history){
      tag.replaceWith(this.history[0].modification_type());
    }else{
      var that=this;
      IMS.query(
        {table:'interaction_history',interaction_id:this.id},
        function(results){
          var history=[];
          for(var row in results){
            history.push(new IMS.Interaction_history(results[row]));
          }
          tag.replaceWith(history[0].modification_type());
          that.history=history;

          // do this next line more intelegently
          $('#interactions').trigger('updateAll');
        }
      )
    }
  }
};
