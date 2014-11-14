IMS.Project=function(data){
  this.data=data;
};
IMS.Project.prototype=new IMS._table();
IMS.Project.prototype._const={
  table:'projects',
  primary_col:'project_id',
  html_class:'projects',

  // everything but processed
  statuses:['normal','high','error','low'],
};

IMS.Project.prototype.html=function(){
  return this.data.project_name;
}

IMS.Project.prototype.publication_report=function(){
  var project_id=this.data.project_id;
  var statuses=this._const.statuses.join('|');
  var that=this;

  IMS.query(
    {table:'project_publications',
     project_id:project_id,
     project_publication_status:statuses},
    function(datum){
      that._publication_report(datum);
    });
}

IMS.Project.prototype._publication_report=function(datum){
  for(var i in datum){
    var data=datum[i];
    var dt='<a class="pmid">' + data.publication_pubmed_id + '</a>';
    $('#project_publications .' + data.project_publication_status).
      append(dt);
  }
  $('#project_publications a').click(function(){
    var pmid=$(this).text();
    IMS.query({table:'publications',publication_pubmed_id:pmid},
              function(data){
                var pub=new IMS.Publication(data[0]);
                IMS.set_publication(pub);
              });
    $('[href=#interaction_tab]').tab('show');
  });
}
