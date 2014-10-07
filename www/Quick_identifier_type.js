IMS.Quick_identifier_type=function(data){
  this.data=data;
}
IMS.Quick_identifier_type.prototype=new IMS._table();
IMS.Quick_identifier_type.prototype._const={
  table:'quick_identifiers',
  primary_col:'quick_identifier_type',
}

/*
 * nonstatic
 */

IMS.Quick_identifier_type.prototype.html=function(){
  return this.data[this._const.primary_key];
}
IMS.Quick_identifier_type.prototype.option=function(selected){
  var out='<option';
  var val=this.primary_id();
  if(val==selected){
    out += ' selected';
  }
  return out+'>'+val+'</option>';
}