IMS.Quick_identifiers=function(data){
  this.data=data;
}
IMS.Quick_identifiers.prototype=new IMS._table();
IMS.Quick_identifiers.prototype._const={
  table:'quick_intentifiers',
  primary_key:'gene_id',
}
IMS.Quick_identifiers.prototype.html=function(){
  var org=this.data.organism_common_name;
  var id                             =
    this.data.systematic_name=='-'   ?
    this.data.quick_identifier_value :
    this.data.systematic_name        ;

  return id+' ('+org+')';
}
