IMS.Interaction_type=function(data){
  this.data=data;
}

/*
 * Strictly static!
 */

// Get the currently selected Interaction_type.primary_id
IMS.Interaction_type.selected_id=function(){
  return $(".interaction_types").val();
},

// run callback with the currently select Interactian_type object as
// as this.
IMS.Interaction_type.async=function(callback){
  var T=IMS.Interaction_type;
  IMS.asyncItem(T,T.selected_id(),function(datum){
    callback.call(new T(datum[0]));
  });
},


// When we change what interaction type we are entering.
IMS.Interaction_type.fieldsets=function(sel){
  var val=$(this).val();

  // clear data about the columny
  var col=$('fieldset.interactions').attr('disabled',true);
  col.find('legend').text('unused');
  col.find('[name=role]').removeAttr('value');

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



IMS.Interaction_type.prototype.organize=function(){
  var got=this.verify_counts();
  if(!got){
    return false;
  }

  var out=[]; // List of really raw interactions
  // out=[
  // [ type_id, {
  //   'participants':[
  //   {
  //    'role_id':###
  //    'participant_type_id':###
  //    'organiszm_id':###
  //    'quick_participant_value':aaa
  //   }.. ]
  //   'ontologies':[
  //    'term_id':####
  //    'type_id':####
  //   ]
  // ]..

  var part_type_id=1; // Gene, will worry about forced later
  var ontologies=[];
  var names=['experimental_systems','throughputs'];
  for(var i in names){
    var name=names[i];
    // see ims/ims.php if you want to change EEaA
    var es_id=$('input:radio[name=' + name + ']:checked').val();
    // Should be an ontology_term_id that points to an Experimental
    // system.
    if(!es_id){
      alert('No ' + name + ' selected');
      return false;
    }
    ontologies.push({'term_id':es_id});
  }

  var type_id=this.primary_id();
  if('Complex'==this.data.interaction_type_name){
    // Here we only ever return one interaction, with who knowns how
    // many participants.
    out[0]=[type_id,{'ontologies':ontologies}];
    var role_id=this.roles[0].primary_id();
    var org_id=got.A.shift();
    var parts=[];

    for(var i in got.A){
      var part={
          role_id:role_id,
          participant_type_id:part_type_id,
          organism_id:org_id,
          quick_participant_value:got.A[i],
      };
      parts.push(part);
    }
    out[0][1]['participants']=parts;
  }else{
    var type_id=this.primary_id();
    var a_org_id=got.A.shift();
    var b_org_id=got.B.shift();
    var a_role_id=this.roles[0].primary_id();
    var b_role_id=this.roles[1].primary_id();

    if(got.A.length==got.B.length){
      while(0!=got.A.length){
        var a_part_value=got.A.shift();
        var b_part_value=got.B.shift();

        var a={
          role_id:a_role_id,
          participant_type_id:part_type_id,
          organism_id:a_org_id,
          quick_participant_value:a_part_value,
        };
        var b={
          role_id:b_role_id,
          participant_type_id:part_type_id,
          organism_id:b_org_id,
          quick_participant_value:b_part_value,
        };

        var i=[type_id,{'participants':[a,b],
                        'ontologies':ontologies}];
        out.push(i);
      }
    }else if(1==got.A.length){
      var a_part_value=got.A.shift();
      var a={
          role_id:a_role_id,
          participant_type_id:part_type_id,
          organism_id:a_org_id,
          quick_participant_value:a_part_value,
      };
      while(0!=got.B.length){
        var b_part_value=got.B.shift();
        var b={
            role_id:b_role_id,
            participant_type_id:part_type_id,
            organism_id:b_org_id,
            quick_participant_value:b_part_value,
        }
        var i=[type_id,{'participants':[a,b],
                        'ontologies':ontologies}];
        out.push(i);
      }
    }else if(1==got.B.length){
      var b_part_value=got.B.shift();
      var b={
          role_id:b_role_id,
          participant_type_id:part_type_id,
          organism_id:b_org_id,
          quick_participant_value:b_part_value,
      }
      while(0!=got.A.length){
        var a_part_value=got.A.shift();
        var a={
            role_id:a_role_id,
            participant_type_id:part_type_id,
            organism_id:b_org_id,
            quick_participant_value:a_part_value,
        };
        var i=[type_id,{'participants':[a,b],
                        'ontologies':ontologies}];
        out.push(i);
      }
    }

  }
  return out;
}

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

/*


IMS.Interaction_type.prototype.add_pairs=function(verified){
  var tbl;
  var A=verified.A;
  var B=verified.B;
  var roleAid=this.roles[0].primary_id();
  var roleBid=this.roles[1].primary_id();

  if(A.length==B.length){
    for(var n in A){
      var a=A[n];
      var b=B[n];
      var i=IMS.pub.get_interaction();
      i.new_interaction_participant(roleAid,Object.keys(a)[0]);
      i.new_interaction_participant(roleBid,Object.keys(b)[0]);
      tbl=i.add_row();
    }
  }else if(1==A.length){
    var a=A[0];
    for(var n in B){
      var b=B[n];
      var i=IMS.pub.new_interaction();
      i.new_interaction_participant(roleAid,Object.keys(a)[0]);
      i.new_interaction_participant(roleBid,Object.keys(b)[0]);
      tbl=i.add_row();
    }
  }else if(1==B.length){
    var b=B[0];
    for(var n in A){
      var a=A[n];
      var i=IMS.pub.new_interaction();
      i.new_interaction_participant(roleAid,Object.keys(a)[0]);
      i.new_interaction_participant(roleBid,Object.keys(b)[0]);
      tbl=i.add_row();
    }
  }else{
    alert('If you see this something went wrong.');
  }
  return tbl;
}
*/