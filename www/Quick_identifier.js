IMS.Quick_identifier=function(data){
  this.data=data;
}
IMS.Quick_identifier.prototype=new IMS._table();
IMS.Quick_identifier.prototype._const={
  table:'quick_intentifiers',
  primary_key:'gene_id',
}
IMS.Quick_identifier.prototype.toString=function(){
  return this.data.quick_identifier_value;
}
IMS.Quick_identifier.prototype.html=function(){
  var org=this.data.organism_common_name;
  var id=this.data.quick_identifier_value;
//  var id                             =
//    this.data.systematic_name=='-'   ?
//    this.data.quick_identifier_value :
//    this.data.systematic_name        ;

  return id+' ('+org+')';
}
