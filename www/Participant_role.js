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
 * nonstatic
 */

IMS.Participant_role.prototype.html=function(){
  return this.data.participant_role_name;
}

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
