IMS.Quick_identifier=function(data){
  this.data=data;

  // for select2
  /*
  this.__defineGetter__('text',function(){
    var out=this.data['quick_identifier_value'];
    console.log(out);
    return out;
  });
   */
}
IMS.Quick_identifier.prototype=new IMS._table();
IMS.Quick_identifier.prototype._const={
  table:'quick_intentifiers',
  primary_col:'gene_id',
}


/*
 * nonstatic
 */

IMS.Quick_identifier.prototype.format_item=function(){
  return this.data.quick_identifier_type
       + ':' + this.toString()
       + ' (systematic:' + this.data.systematic_name
       + ', official:' + this.data.official_name
       + ')'
  ;

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
