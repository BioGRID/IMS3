IMS.Interaction_type=function(data){
  this.data=data;
}

/*
 * Strictly static!
 */

// When we change what interaction type we are changeing.
IMS.Interaction_type.fieldsets=function(sel){
  var val=$(this).val();

  $('fieldset.interactions').
    attr('disabled',true).
    removeAttr('id').
    find('legend').text('unused');

  IMS.asyncItem
  (IMS.Interaction_type,val,
   function(datum){
     var me=new IMS.Interaction_type(datum[0]);

     me.roles_forEach(function(role){
       role.fieldset();
     });
   });
}


/*
 * static, but ok to call from an instance.
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

// executes the act callback on each role.  If it doesn't know what
// roles we have yet it will fetch them and possably call them async.
IMS.Interaction_type.prototype.roles_forEach=function(act){

  if(this.roles){
    this.forEach(act);
    return;
  }

  // Numbers in the list returned by this function are
  // participant_role_id as defined in the participant_roles table, from
  // the Particiant.sql file.  Check out Participant_role.js too.
  var role_ids;
  switch(this.data.interaction_type_name){
    case('Complex'):
    role_ids=[1]; // unspecified
    break;
    default:
    role_ids=[2,3]; // bait, hit
    break;
  }

  // holdes the roles.
  this.roles=[];
  var that=this;
  for(var i in role_ids){
    if(IMS.Participant_role.s[role_ids[i]]){
      var role=IMS.Participant_role.s[role_ids[i]];
      this.roles.push(role);
      act(role,i,role_ids);
    }else{
      IMS.asyncItem(IMS.Participant_role,role_ids[i],function(r){
        var role=new IMS.Participant_role(r[0]);
        that.roles.push(role);
        act(role,i,role_ids);
        IMS.Participant_role.s[role.primary_id()]=role;
      });
    }
  }
} // roles_forEach



// Sucks data out of the forms.  Checks that the number of
// participants entered in each column is valid.  If not alerts() the
// user.  if it is it returs a datastructure of the content thus:
// {
//  'A'=[org_id,part1,[part2,[part3]...]],
//  'B'=[org_id,part1,[part2,[part3]...]]
// }
// Or just 'A'=... if a complex.
IMS.Interaction_type.prototype.verify_counts=function(){
  var pps=[]; // potential participants by role
  var org=[]; // organism_ids by role
  var r=this.roles_forEach(function(role,i){
          pps[i]=role.participants();
          org[i]=role.organism_id();
        });

  if(this.data.interaction_type_name == 'Complex'){
    if (1 != pps.length){
      alert('Only one list of Participants please (bug).');
      // hopefully we never get here as the other column should be
      // disabled.
      return false;
    }

    if (0 == pps[0].length){
      alert('No Complex Participants entered.');
      return false;
    }

  }else{
    if (2 != pps.length){
      alert('Strictly two lists of participants (bug).');
      return false;
    }

    var A=pps[0].length;
    var B=pps[1].length;

    if ( (A==0) || (B==0) ) {
      alert("Participant lists can't be empty.");
      return false;
    }

    if ( (A!=B) && ((A!=1) && (B!=1)) ){
      alert('Participant list count missmatch.');
      return false;
    }

  }

  // as pps and org should be the same length we can use the same
  // index to loop through them.
  var cns=['A','B']; // column names
  var out={}
  for(var i in pps){
    out[cns[i]]=[org[i]].concat(pps[i]);
  }
  return out;
}

// takes output from true verify_count() and checks them with the
// database.
IMS.Interaction_type.prototype.verify_db=function(verified,success){
      $.ajax(
        {
          type:'POST',
          url:'verify.php',
          dataType:'json',
          data:verified
        }
      ).success(function(r){
        var ok=r.ok;
        delete r.ok;
        if(0==Object.keys(r).length){
          // all worked!
          success(ok);
        }else{
          // Make more user friendly error message.
          alert(JSON.stringify(r));
        }

      }).fail(function(){
        alert('There is a bug verifying genes, please complain.');
      });



}