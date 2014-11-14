IMS.User=function(data){
  this.data=data;
  this.project;
  this.projects=[];
};
IMS.User.prototype=new IMS._table();
IMS.User.prototype._const={
  table:'users',
  primary_col:'user_id',
}
IMS.User.prototype.html=function(){
  return '<code>' + this.data.user_name + '</code>'
}

// Populate the project page
IMS.User.prototype.project=function(){
  var that=this;
  IMS.query(
    {table:'project_users',
     user_id:this.id,
    },function(raw){
        project_ids=[];
        for(var i in raw){
          project_ids.push(raw[i].project_id);
        }
        IMS.query(
          {table:'projects',
           project_id:project_ids.join('|'),
          },function(raw){
              that._project(raw);
            }
        );
      }
  );
}

IMS.User.prototype._project=function(raw){
  var project_id=this.data.project_id;
  var sel=IMS.Project.prototype.$('select');
  for(var i in raw){
    var p=new IMS.Project(raw[i]);
    this.projects.push(p);
    if(project_id==p.id){
      var organism_id=p.data.organism_id;
      IMS.populate_select(IMS.Quick_organism,{selected:organism_id});
      p.publication_report();
      this.project=p;
    }
    sel.append(p.option_html(project_id));
  }
}

