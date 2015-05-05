IMS.Ontology=function(data){
  this.data=data;
}

IMS.Ontology.prototype=new IMS._table();
IMS.Ontology.prototype._const={
  table:'ontologies',
  primary_col:'ontology_id',
  html_class:'ontologies'
}

IMS.Ontology.fieldsets=function(sel){
  var r={table:IMS.Ontology.prototype.table()};
  var pc=IMS.Ontology.prototype.primary_col();
  r[pc]=$(this).val();

  IMS.cache(r,function(row){
    var o=new IMS.Ontology(row[0]);
    var iot=$('.interaction_ontology_types')

    iot.find('option').prop('disabled',true);
    o.data.interaction_ontology_type_shortcodes.forEach(function(sc){
      iot.find('.iot_'.concat(sc)).prop('disabled',false);

      if(null===iot.val()){
        iot.val(iot.find('option:enabled').val());
      }
    })
  },pc);
}

IMS.Ontology.prototype.html=function(){
  return this.data.ontology_name;
}
