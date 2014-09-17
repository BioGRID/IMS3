IMS.Publication=function(data){
  this.data=data;

  // decrements on newly created interactions
  this.new_id=0;

  // current selected interaction
  this.interaction=null;

  // Move this up to IMS._table if we need to use select2 for a
  // different items other then publication.
  this.__defineGetter__('text',function(){
    return this.pmid();
  });
},

IMS.Publication.prototype=new IMS._table();
IMS.Publication.prototype._const={
  primary_col:'publication_id'
}
IMS.Publication.prototype.format_item=function(){
  return this.data.publication_pubmed_id + ' - ' +
    this.data.publication_article_title;
}
IMS.Publication.prototype.pmid=function(){
  return this.data['publication_pubmed_id'];
}
