IMS.Participant_role=function(data){
  this.data=data;
}
IMS.Participant_role.prototype=new IMS._table();
IMS.Participant_role.prototype._const={
  table:'participant_roles',
  primary_col:'participant_role_id',
  //html_id:'participant_role', // dep
  html_class:'participant_role'
}

/*
 * Strictly static.
 */

// A place to hold all roles by pk, so we don't make too many dup
// instances.
IMS.Participant_role.s={};

/*
 * static
 */

// Which column should this role be represented in the Create
// Interaction section.  The switch in an participant_role_id SQL
// column.  See Participant.sql and Interaction_type.js files.
IMS.Participant_role.prototype.col=function(){
  var col='A';
  switch(this.primary_id()){
    case '3': // hit
    col='B';
  }
  return $('fieldset.col'+col);
}

/*
 * nonstatic
 */

IMS.Participant_role.prototype.html=function(){
  return this.data.participant_role_name;
}

/*
 * Still nonstatic, this items are to extract data from the HTML
 * forms.
 */

// Returns the potentital participants in fieldset's textarea that, if
// verified, will have this role.
IMS.Participant_role.prototype.participants=function(){
  var out=this.col().find('textarea').val().trim().split(/\s+/);

  if((1==out.length) && (0==out[0].length)){
    return [];
  }

  return out;
}

// Returns the current organism_id of the select organism.
IMS.Participant_role.prototype.organism_id=function(){
  return this.col().find('.quick_organism').val();
}

// Set up the fieldsets to reflect what we want.
IMS.Participant_role.prototype.fieldset=function(){
  var col= this.col().attr('disabled',false);
  col.find('legend').text(this.html());
  col.find('[name=role]').attr('value',this.primary_id());
}
