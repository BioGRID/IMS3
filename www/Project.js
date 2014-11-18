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
  sel.html('');

  var by_status={};

  // Put each publication in it's place.
  for(var i in datum){
    var data=datum[i];
    var status=data.project_publication_status;
    var pmid=data.publication_pubmed_id;

    if(by_status[status]){
      by_status[status].push(pmid);
    }else{
      by_status[status]=[pmid];
    }
  }

  for(var s in by_status){
    sel.append('<h2>'+s+'</h2>');

    var lis='';
    by_status[s].forEach(function(pmid){
      lis+='<li class="pubmed">'+pmid+'</li>';
    });
    sel.append('<ul class="list-inline">'+lis+'</ul>');
  }


  // if we click on a publication switch the tabe to that page, and
  // load the publication.  Select2 is giving me some problems but I
  // wanna get this up for for now.
  sel.find('.pubmed').click(function(){
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
