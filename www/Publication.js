IMS.Publication=function(data){
  this.data=data;

  // decrements on newly created interactions
  this.new_id=0;

  this.interactions={};  // list of interactions, including new ones
  this.interaction=null; // current selected interaction

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
  IMS.Interaction_type.async(function(){
    // get a list of valid interaction pairs
    var got=this.organize();
    var request={
      type:'POST',
      url:'commit.php',
      dataType:'json',
      data:{'interactions':got},
    }
    $.ajax(request).
      fail(function(){
      alert('something when wrong commiting the interactions');
    }).success(function(){
      alert('yea');
    });
  });
}
