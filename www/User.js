IMS.User=function(data){
  this.data=data;
  this.project;
  this.projects={};
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

  var that=this; // used if project is changed
  var sel=IMS.Project.prototype.$('select').
      change(function(){
            var p=that.projects[$(this).val()];
            p.publication_report();
            that.project=p;
          });
  for(var i in raw){
    var p=new IMS.Project(raw[i]);
    this.projects[p.id]=p;
    if(project_id==p.id){
      this.project=p.publication_report();
    }
    sel.append(p.option_html(project_id));
  }
}

