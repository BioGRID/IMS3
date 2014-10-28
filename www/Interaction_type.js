IMS.Interaction_type=function(data){
  this.data=data;
}

/*
 * Really static, but not to be called by an instance.
 */


// When we change what interaction type we are changeing.
IMS.Interaction_type.fieldsets=function(sel){
  var val=$(this).val();
  IMS.asyncItem
  (IMS.Interaction_type,val,
   function(datum){
         var me=new IMS.Interaction_type(datum[0]);
         me.fieldsets();
   });
}


/*
 * static
 */

IMS.Interaction_type.prototype=new IMS._table();
IMS.Interaction_type.prototype._const={
  table:'interaction_types',
  primary_col:'interaction_type_id',
  html_class:'interaction_types'
}

/*
 * nonstatic
 */

IMS.Interaction_type.prototype.html=function(){
  return this.data.interaction_type_name;
}

IMS.Interaction_type.prototype.fieldsets=function(){
  var A=$('fieldset.colA');
  var B=$('fieldset.colB');

  // The items 'unspecified', 'bait', and 'prey' are
  // participant_role_name entries.  If they change in the database,
  // you will have to change them here.  But there is no connection in
  // the database about what interaction_type wants what
  // participant_role.

  switch(this.data.interaction_type_name){
    case('Complex'):
    A.attr('disabled',false);
    A.find('legend').text('unspecified');
    B.attr('disabled',true);
    B.find('legend').text('disabled');
    break;
    case('Protein-Protein'):
    A.attr('disabled',false);
    A.find('legend').text('bait');
    B.attr('disabled',false);
    B.find('legend').text('prey');
    break;
    default:
    alert('Unknown participant_type selected.');
  }
}
