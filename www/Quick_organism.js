IMS.Quick_organism=function(data){
  this.data=data;
}
IMS.Quick_organism.prototype=new IMS._table();
IMS.Quick_organism.prototype._const={
  table:'quick_organisms',
  primary_key:'organism_id',
}
IMS.Quick_organism.prototype.html=function(){
  return this.data.organism_common_name;
}