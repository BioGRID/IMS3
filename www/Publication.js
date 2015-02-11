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
