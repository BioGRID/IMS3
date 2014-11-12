IMS.Quick_organism=function(data){
  this.data=data;
}
IMS.Quick_organism.prototype=new IMS._table();
IMS.Quick_organism.prototype._const={
  table:'quick_organisms',
  primary_col:'organism_id',
  default:"559292", // to match with this.id
  html_class:'quick_organism',
}

/*
 * nonstatic
 */

IMS.Quick_organism.prototype.html=function(){
  return this.data.organism_display_name;
}
