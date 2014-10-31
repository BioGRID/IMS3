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

/*
 * static
 */

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
    'modification_type',
  ];
};


// types should be loaded at startup, so I'm not worried about them
// not being there.
IMS.Interaction.prototype.type=function(){
  if(!this._type){
    this._type=IMS.getItem(IMS.Interaction_type,this.data.interaction_type_id);
  }
  return this._type;
}

// Stage the data if it's valid.
IMS.Interaction.prototype.stage=function(){
  t=this.type()
  var ok=t.verify_counts();
  if(ok){
    // if we are here the counts should be correct, now we need to
    // check the database to make sure the participants are valid.
    var that=this;
    t.verify_db(ok,function(verified){
      // now we assume everything in verifies is, um, verified.
      that._stage(verified);
    });
  }
}

// Blindly add the data.  Do this next
IMS.Interaction.prototype._stage=function(v){
  alert(JSON.stringify(v));
}
