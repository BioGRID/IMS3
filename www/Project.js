IMS.Project=function(data){
  this.data=data;
};
IMS.Project.prototype=new IMS._table();
IMS.Project.prototype._const={
  table:'projects',
  primary_col:'project_id',
  html_class:'projects',

  // everything but processed
  statuses:['normal','high','error'], // IMS2 only
  //statuses:['normal','high','error','low'], now in IMS3!
};

IMS.Project.prototype.html=function(){
  return this.data.project_name;
}

IMS.Project.prototype.publication_report=function(){
  var project_id=this.data.project_id;
  var statuses=this._const.statuses.join('|');
  var that=this;

  // Change the default organism
  var organism_id=this.data.organism_id;
  IMS.populate_select(IMS.Quick_organism,{selected:organism_id});

  IMS.query(
    {table:'project_publications',
     project_id:project_id,
     project_publication_status:statuses},
    function(datum){
      that._publication_report(datum);
    });

  return this;
}

IMS.Project.prototype._publication_report=function(datum){
  // datum contains items from the project_publication table along
  // with the project_pubmed_id.

  var sel=$('#project_publications');
  // Clear the line incase we are changing projects.
  sel.find('p').html('');

  // Put each publication in it's place.
  for(var i in datum){
    var data=datum[i];
    var dt='<a class="pmid">' + data.publication_pubmed_id + '</a>';
    sel.find('.' + data.project_publication_status).append(dt);
  }

  // if we click on a publication switch the tabe to that page, and
  // load the publication.  Select2 is giving me some problems but I
  // wanna get this up for for now.
  $('#project_publications a').click(function(){
    var pmid=$(this).text();
    IMS.query({table:'publications',publication_pubmed_id:pmid},
              function(data){
                $('#pubmed').select2('search',data[0].publication_pubmed_id);
                //var pub=new IMS.Publication(data[0]);
                //IMS.set_publication(pub);
              });
    $('[href=#interaction_tab]').tab('show');
  });
}
