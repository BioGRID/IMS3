IMS.Interaction=function(data){
  this.data=data;
  this.new_id=0;

  this.participants={};  // list of participants (er, Interaction_participants)
  this.participant=null; // selected participant (ibid.)
}

IMS.Interaction.prototype=new IMS._table();
IMS.Interaction.prototype._const={
  table:'interaction',
  primary_col:'interaction_id',
  html_class:'interactions'
};

IMS.Interaction.prototype.dd=function(dt){
  var out=IMS._table.prototype.dd.call(this,dt);
  if('ontologies'==dt){
    if(0!==parseInt(out,10)){
      return '<button data-toggle="modal" data-target="#ontologies">'+out+'</button>';
    }
  }
  return out;
};


/*
 * static
 */

IMS.Interaction.prototype.dts=function(){
  return [
    'interaction_id',
    'bait','hit',  // see also
    //'participant_hash',
    //'publication_id',
    //'interaction_type_id',
    'interaction_type',
    'interaction_status',
    //'interaction_source_id',
    'interaction_source',
    'ontologies',
    'modification_type',
    'interaction_note',
  ];
};

/*
 * non static
 */

IMS.Interaction.prototype.new_interaction_participant=function(role_id,participant_id){
  var ip=new IMS.Interaction_participant({
    interaction_participant_id:--this.new_id,
    interaction_id:this.primary_id(),
    participant_id:participant_id,
    participant_role_id:role_id,
    interaction_participant_status:'active',
    interaction_participant_addeddate:'not added',
  });
  this.participants[ip.primary_id()]=ip;
  return ip;
}

IMS.Interaction.prototype.add_row=function(){
  var tbl=this.$('table');
  var thead=tbl.find('thead');
  var tbody=tbl.find('tbody');
  IMS.add_row(thead,tbody,this).click(IMS.click_interaction);
  //tbl.trigger('update');
  return tbl;
}

/*
 * Overide the default also finction to to something with bait and hit
 * entries.
 */
IMS.Interaction.prototype.also=function(dt){
  if(-1!=['bait','hit']){
    return '<span class="bg-danger">'+dt+'</span>';
  }
  return false;
}
