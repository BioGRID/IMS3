IMS.Publication=function(data){
  this.data=data;

  // decrements on newly created interactions
  this.new_id=0;

  this.interactions={};  // list of interactions, including new ones
  this.interaction=null; // current selected interaction
  this.modification_type='ACTIVATED'; // current type of modificatinos being displayed
  this.modification_types={};

  // Move this up to IMS._table if we need to use select2 for a
  // different items other then publication.
  /*
  this.__defineGetter__('text',function(){
    var out=this.pmid();
    console.log(out);
    return out;
  });
   */
},

IMS.Publication.prototype=new IMS._table();
IMS.Publication.prototype._const={
  primary_col:'publication_id'
}

/*
 * static
 */

// Verbose description mostly used for select2
IMS.Publication.prototype.format_item=function(){
  return this.data.publication_pubmed_id + ' - ' +
    this.data.publication_article_title;
}
IMS.Publication.prototype.pmid=function(){
  return this.data.publication_pubmed_id;
}

IMS.Publication.prototype.commit=function(){
  // first we get the interaction_type
  var it_id=$('.interaction_types').val();
  var pub_id=this.primary_id(); // not pmid
  IMS.Interaction_type.async(function(){
    // get a list of valid interaction pairs
    var got=this.organize();
    if(!got){
      // It's up to Interaction_type.js to gripe if something is wrong.
      return;
    }
    var data={};
    data[pub_id]=got;
    var request={
      type:'POST',
      url:'commit.php',
      dataType:'json',
      data:data,
    }
    $.ajax(request).
      fail(function(htr){
      alert(htr.responseText);
    }).success(function(){
      // We got new interactions!  Retset the publications.
      IMS.reset_publication();
    });
  });
}

/*
 * non-static
 */

/*
IMS.Publication.prototype.current=function(interaction){
  return interaction.data.modification_type==this.modification_type;
}
*/

IMS.Publication.prototype.remember=function(i){
  this.interactions[i.id]=i;
  var mt=i.data.modification_type;
  if(!this.modification_types[mt]){
    this.modification_types[mt]={};
  }
  this.modification_types[mt][i.id]=i;

  var mtt=$('#modification_type'); // mt tag
  var name='name="modification_type"';
  var value='value="' + mt + '"';
  var r=mtt.find('[' + name + '][' + value +']');

  if(0==r.length){
    var checked='';
    if(this.modification_type==mt){
      checked=' checked';
    }

    var label=$('<label><input type="radio" '
               + name + ' ' + value + checked + '>'
               + mt + ' (<span>1</span>)</label>');
    mtt.append(label);
    var pub=this;
    label.change(function(){
      var i=$(this).find('input');
      pub.modification_type=i.val();
      IMS.reset_publication();
    });
  }else{
    mtt.find('span').text(Object.keys(this.modification_types[mt]).length);
  }
}

IMS.Publication.prototype.fetch_interactions=function(){
  var pub=this;
  IMS.query({publication_id:this.primary_id(),table:'interactions'},
            function(results){
              var inter=IMS.redo_table(results,IMS.Interaction,function(i){
                          pub.remember(i);
                          if(i._tr){
                            i._tr.click(IMS.click_interaction);
                          }
                        });
            }

           );
}
