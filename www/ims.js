// Items that start with a capitol letter are reserved for table
// objects related to the database.
IMS={

  // Stores the current IMS.Publication object
  pub:null,
  user:null,

  /*
   * First, a bunch af utilities.
   */

  // get a unique list of items via Array.prototype.filter()
  unique:function(v,i,a){
    return i==a.indexOf(v);
  },

  // Report errors, usually from the query.php script, on the log page.
  report_messages:function(messages){
    for(var row in messages){
      var msg=messages[row];
      var t=IMS.php_error(msg['type']);

      alert(t.msg + ': ' + msg['message'] + ' in ' + msg['file'] + ' on line ' + msg['line']);
    }


    /*
    // Add the number of new messages to the current message count.
    mc=$('.log-count');
    count=Number(mc.text());
    count+=messages.length;
    mc.text(count);

    // prepend new messages to list
    list=$('#log');
    for(var row in messages){
      var msg=messages[row];
      var t=IMS.php_error(msg['type']);
      var html='<p><strong class="text-'+t.class+'">'+t.msg+'</strong>: '
              +msg['message']+' in <code>' + msg['file'] + '</code> '
              +'on line ' + msg['line'] + '</p>';
      list.prepend(html);
    }
    list.prepend("<h2>"+(new Date().toString())+"</h2>");
     */
  },

  // Returns PHP error codes as text, along with bootstrap class.
  php_error:function(errno){
    switch(errno){
      case     1:return {msg:'E_ERROR'            ,class:'danger'};
      case     2:return {msg:'E_WARNING'          ,class:'warning'};
      case     4:return {msg:'E_PARSE'            ,class:'danger'};
      case     8:return {msg:'E_NOTICE'           ,class:'info'};
      case    16:return {msg:'E_CORE_ERROR'       ,class:'danger'};
      case    32:return {msg:'E_CORE_WARNING'     ,class:'warning'};
      case    64:return {msg:'E_COMPILE_ERROR'    ,class:'danger'};
      case   128:return {msg:'E_COMPILE_WARNING'  ,class:'warning'};
      case   256:return {msg:'E_USER_ERROR'       ,class:'danger'};
      case   512:return {msg:'E_USER_WARNING'     ,class:'warning'};
      case  1024:return {msg:'E_USER_NOTICE'      ,class:'info'};
      case  2048:return {msg:'E_STRICT'           ,class:'danger'};
      case  4096:return {msg:'E_RECOVERABLE_ERROR',class:'danger'};
      case  8192:return {msg:'E_DEPRECATED'       ,class:'info'};
      case 16384:return {msg:'E_USER_DEPRECATED'  ,class:'info'};
      case 30719:return {msg:'E_ALL'              ,class:'danger'};
    }
    return {msg:'E_UNKNOWN('+errno+')',class:'danger'};
  },

  /*
   * User authenication functions
   */

  // Just delete the cookies.
  logout:function(){
    IMS.user=null;
    var date=new Date();
    date.setTime(0);
    var expires='=; expires='+date.toGMTString();
    document.cookie='auth'+expires;
    document.cookie='name'+expires;

    // only show user class items to logged in people.
    $('.user').addClass('hidden');
    IMS.login_html();
  },

  // Try to log in.
  login:function(but){
    var user=$(but).siblings('[name=name]').val();
    var pass=$(but).siblings('[name=password]').val();
    $.ajax(IMS.ajax_query({name:user,pass:pass},
                          {type:'POST',url:'user.php'}))
    .success(IMS.loggedin_html);


  },

  // What to print if we are not logged in.
  login_html:function(){
    $('#user').html('Username: <input type="text" name="name"> '
                   +'Password: <input type="password" name="password"> '
                   +'<button onclick="IMS.login(this)">Login</button>');
  },

  // This should only get run if we are sure we are logged it.
  loggedin_html:function(raw){
    var user=new IMS.User(raw);
    IMS.user=user;

    // The JavaScript cookie interface really sucks.
    //var c='; '+document.cookie;
    //var kv=c.split('; name=');
    //var user=kv.pop().split(';').shift();

    // show logged in users some hidden stuff.
    $('.user').removeClass('hidden');

    $("#user").html
    ('Logged in as ' + user.html()
    +' <button onclick="IMS.logout()">Logout</button>');

    user.project();
  },

  /*
   * Abstracted access to the query.php CGI script.
   */

  // Returns a standard argument suitable for use is a $.ajax call to
  // the query.php CGI. This is abstracted this way to make select2
  // happy.
  ajax_query:function(request,also){
    var out={
      type:'GET',
      url:'query.php',
      dataType:'json',
      //data:request,
      //table:request.table,
      cache:true,
    };
    if(request){
      out.data=request;
    }
    if(also){
      for(var key in also){
        out[key]=also[key];
      }
    }
    return out;
  },

  // Do the ajax call
  query_count:0,
  query:function(request,act){
    if(3>IMS.query_count){ // only 3 queries at a time
      IMS.query_count++;
      //console.log(IMS.query_count,'up');
      $.ajax(IMS.ajax_query(request,IMS.act)).success(
        function(data){
          IMS.query_count--;
          //console.log(IMS.query_count,'up');
          IMS.report_messages(data.messages);
          act(data.results);
        });
    }else{
      // wait a half second and try again.
      setTimeout(IMS.query,500,request,act);
    }
  },

  /*
   *  Where to store what item.  The primary_key var is actually the
   * name of the primary_key column of an SQL table, to the
   * primary_key value.
   */
  whichStore:function(primary_col){
    var store=localStorage;
    switch(primary_col){
      // There could be a bunch of participants, so lets not remember
      // them but for this session.
      case 'participant_id':
      store=sessionStorage;
    }
    return store;
  },


  _storeItems:function(datum,primary_col){
    var store=IMS.whichStore(primary_col);
    for(var i in datum){
      var data=datum[i];

      // Create a place to store the data incase we don't already have
      // a place.
      var have=store.getItem(primary_col);
      have=(null==have)?{}:JSON.parse(have);

      // for now we only can cache one item at a time.
      have[data[primary_col]]=data;
      store.setItem(primary_col,JSON.stringify(have));
    }
  },

  asyncItem:function(Table,pk,callback){
    var r={table:Table.prototype.table()};
    var pc=Table.prototype.primary_col();
    r[pc]=pk;
    IMS.cache(r,callback,pc);
  },

  // Returns the on item from a local store.  If not it store it
  // carps.
  getItem:function(Table,pk){
    var pc=Table.prototype.primary_col();
    var store=IMS.whichStore(pc);
    var have=store.getItem(pc);
    if(have){
      have=JSON.parse(have);
      var out=have[pk];
      if(out){
        return new Table(out);
      }
    }
    //console.log(pc);
    alert('Request for ' + pc + " not loaded from database or doesn't exist.");
  },


  /*
   * Send a request that will only get one row.  Checks a store to see
   * if we already have it.
   */
  cache:function(request,act,primary_key){
    var store=IMS.whichStore(primary_key);
    var have=store.getItem(primary_key);

    have=(null==have)?{}:JSON.parse(have);
    if(have[request[primary_key]]){
      return act([have[request[primary_key]]]);
    }else{
      IMS.query(request,function(datum){
        // Hurry up and update the user feedback.
        act(datum);

        IMS._storeItems(datum,primary_key);
      });
    }
    return false;
  },

  /*
   * Weird stuff for display localStorage, hopefully sessionStorage in
   * the future too.
   */

  localStorage_dl:function(){
    $('#localStorage .modal-body').html(IMS._localStorage_dl())
  },
  _localStorage_dl:function(){
    var out='<dl class="dl-horizontal">';
    Object.keys(localStorage).forEach(function(dt){
      dd=localStorage.getItem(dt).replace(/,/g,',&#8203;');
      out+='<dt>'+dt+'</dt><dd>'+dd+'</dd>';
    });
    return out+'</dl>';
  },


  /*
   * Updating tables, et al.
   */

  // Accepts a Publication object, and make it what we are looking at.
  set_publication:function(pub){
    // clear some things from the last publication
    $(".participants thead").html('');
    $(".participants tbody").html('');
    $(".participants .footnotes *").addClass('hide');

    IMS.pub=pub;
    $("#publication").html(pub.select('publication_abstract'));

    // Now get the interactions
    IMS.query({publication_id:pub.primary_id(),table:'interactions'},
              IMS.update_interactions);
  },

  reset_publication:function(){
    if(IMS.pub){
      // a little weird but it works.
      IMS.set_publication(IMS.pub);
    }
  },

  // try to get an active object from a HTML tag burried in a
  // itemscope.
  active:function(tag){
    var item=tag.parentsUntil('tr[itemscope]').parent();
    console.log( IMS[item.attr('itemtype')] );
    var pk=IMS[item.attr('itemtype')]
           ._active[item.find('[itemprop=primary-key]').text()];
    return pk;
  },

  update_danger:function(tbl){
    tbl.find('.bg-danger').each(function(){
      var tag=$(this);
      var prop=tag.parent().attr('itemprop');
      //console.log(prop);

      // Not sure how portable this is
      var Table=IMS[prop.charAt(0).toUpperCase()+prop.slice(1)];

      if(Table){
        var col=Table.prototype.primary_col();
        var val=tag.text();
        if(Table.prototype.ok(col,val,tag)){
          // Stuff we can figure out without actually accessing the
          // object in scope.
          var primary_col=col;
          var request={table:Table.prototype.table()};
          request[primary_col]=val;
          IMS.cache(request,function(raw){
            tag.replaceWith(new Table(raw[0]).html());
          },primary_col);
        }
      }

    });
  },

  //
  add_row:function(thead,tbody,result){
    if(0==thead.children().length){
      thead.append(result.th());
    }
    var td=$($.parseHTML(result.td()));
    tbody.append(td);
    result._tr=td;
    return td;
  },

  // Abstracted was to dump results from query.php into an HTML table.
  redo_table:function(results,Table){
    // get the HTML table
    var tbl=Table.prototype.$('table');

    var tbody=tbl.find('tbody');
    // If the table is under control by dataTable, clear and destroy
    // it! Otherwise, just make sure the body is empty.

    if(tbl.is('.dataTable')){
      // We don't use $.fn.DataTable.isDataTable(tbl)) because I want
      // this to work with and without DataTable loaded.
      tbl.DataTable().clear().destroy();
    }else if(tbl.is('.tablesorter')){
      tbl.trigger('destroy');
    }
    tbody.html('');

    // clear the header.
    var thead=tbl.find('thead').html('');
    tbl.find('.footnotes *').addClass('hide');

    // Populate the table with results.
    var out={};
    for(var row in results){
      var i=results[row];
      if(!i.table){
        i=new Table(results[row]);
      }
      IMS.add_row(thead,tbody,i);
      out[i.id]=i;
    }

    // So we can use some CSS to align the numbers right but still
    // keep them, more or less, left.
    tbody
    .find('.primary-key')
    .wrapInner('<span></span>');

    var that=this;
    //tbl.dataTable();

    tbl.tablesorter({
      theme: "bootstrap",
      widthFixed: true,
      headerTemplate: '{content} {icon}',
      widgets: ["uitheme","zebra"],
    })
    .tablesorterPager({container:tbl.prev()});

    tbl.on('draw.dt',function(){
      that.update_danger(tbl);
    });
    this.update_danger(tbl);

    // return created items
    return out;
  }, // redo_table

  populate_select:function(Table,named){
    var selected;
    var callback;
    if(named){
      selected=named['selected'];
      callback=named['callback'];
    }

    var sel=Table.prototype.$('select');

    IMS.query
    ({table:Table.prototype.table()},
     function(results){
       IMS._storeItems(results,Table.prototype.primary_col());

       var opts='';
       for(row in results){
         var result=new Table(results[row]);
         opts+=result.option_html(selected);
       }
       if(0==sel.length){
         alert('Unable to populate ' + Table.prototype._const.table);
       }else{
         sel.html('').append(opts);
         if(callback){
           callback.call(sel);
         }
       }
     });

    // returned item might not be filled yet, but the above IMS.query
    // should fix that.
    return sel;
  },


  click_interaction:function(e){
    // get the IMS.Interaction object of the clicked interaction
    var interaction_id=$(this).find('[itemprop=primary-key]').text();
    var interaction=IMS.pub.interactions[interaction_id];

    // Toggle highlighted tr
    if(IMS.pub.interaction){
      // removing highlighting if on is active.
      IMS.pub.interaction._tr.removeClass('active');
    }
    // set the current active interaction
    IMS.pub.interaction=interaction;
    interaction._tr.addClass('active');

/*
    // If we click on ontologies we want to pop up a window of some kind.
    if('ontologies'==e.target.getAttribute('itemprop')){
      console.log(e.target);
    }
*/

    if(0<Object.keys(interaction.participants).length){
      // If we already have participants, display them
      IMS.redo_table(interaction.participants,IMS.Interaction_participant);
    }else if(0<interaction_id){
      // If we don't have any participants, and we are saved in the
      // database, che5Ack the database for participants.
      IMS.query(
        {
          interaction_id:interaction_id,
          table:'interaction_participants'
        },function(results){
            interaction.participants=
              IMS.redo_table(results,IMS.Interaction_participant);
          }
      );
    }else{
      // New interaction! Lets just clean the participant table.
      IMS.redo_table([],IMS.Interaction_participant);
    }

  },

  update_interactions:function(results){
    var inter=IMS.redo_table(results,IMS.Interaction);
    for(var action in inter){
      var i=inter[action];
      IMS.pub.interactions[i.id]=i;
      i._tr.click(IMS.click_interaction);
    }

  },


  /*
   * Functions I think should be in other libraries.
   */

  // Sure Twitter Bootstrap has dropdown menus, but they don't change
  // what they are displaying!  See #publication in home.php for
  // usage.
  select:function(select){
    // Might have to change this to using something like data-toggle,
    // but for now this will do.
    var from=$(select.nextSibling);
    from.find('div').addClass('hide');
    from.find('#'+select.value).removeClass('hide');
  },


  /*
   * To hold prototype for row data.
   */
  _table:function(data){
    if(data){
      this.data=data;
    }

    // Here to make select2 happy
    this.__defineGetter__('id',function(){
      return this.primary_id();
    });

  },

}


IMS._table.prototype={

  /*
   *  stuff that can be usen statically.
   */

  // Returns the SQL table.
  table:function(){
    return this._const.table;
  },

  // Return's the SQL table primary key column.
  primary_col:function(){
    out=this._const.primary_col;
    if(!out){
      console.log('No primary_col specified.');
    }
    return out;
  },

  // using $ to imply it returns jQuery tags.
  $:function(tag){
    return $(tag+'.'+this._const.html_class);
  },

  /*
  tag_html:function(){
    return $('#' + this._const.html_id);
  },
  tag_select:function(){
    var clazz=this._const.html_class
    return $('select.' + clazz);
  },
   */

  // To check if we want to do something weird in a column in the
  // IMS.update_danger() function.
  ok:function(col,val,tag){
    return true;
  },

  /*
   * instance specific functions.
   */

  type:function(){
    table=this.table();
    return table.charAt(0).toUpperCase()+table.slice(1);
  },
  // Returns the items contained in the primary_col of the row.
  primary_id:function(){
    return this.data[this.primary_col()];
  },
  // unique value for this suitable for use in an HTML class or id
  // attribute.
  unique_html:function(){
    return this.primary_col() + this.primary_id();
  },

  // Returns HTML suitable for inlined usage.
  html:function(){
    return this.primary_col()+'='+this.primary_id();
  },
  option_html:function(selected){
    //var sel=(this._const.default==this.id)?' SELECTED':'';
    var sel=(selected==this.id)?' SELECTED':'';

    return '<option' + sel
         + ' value="' + this.primary_id() + '">'
         + this.html() + '</option>';
  },

  // Return a list of definition term names, that then can be fed to
  // the dt function.
  dts:function(){
    return Object.keys(this.data);
  },
  dd:function(dt){
    if(this.data[dt]){
      return this.data[dt];
    }else{
      var dt_id=this.data[dt+'_id'];
      if(dt_id){
        return '<span class="bg-danger">'+this.data[dt+'_id']+'</span>';
      }else if(null===dt_id){
        return '<i>null</i>';
      }
    }
    return '<span class="bg-danger">This is a bug &#10233 &#128027</span>';
  },


  /*
   * Output items useable with the IMS.select function.
   */
  select:function(show){
    var divs='';
    var options='';
    this.dts().forEach(function(dt){
      var clazz='hide';
      var selected='';
      if(show==dt){
        clazz='';
        selected=' selected';
      }
      var dd=this.dd(dt);
      divs+='<div class="'+clazz+'" id="'+dt+'">'+dd+'</div>';
      options+='<option'+selected+'>'+dt+'</option>';
    },this);
    return '<select onchange="IMS.select(this)">'+options
         +'</select><div>'+divs+'</div>';
  },

  /*
  clazz:function(dt){
    switch(dt){
      case this._const.primary_key:return ' class="primary-key"';
    }
    return '';
  },
   */

  itemprop:function(dt){
    if(dt==this.primary_col()){
      return ' itemprop="primary-key"';
    }
    return ' itemprop="' + dt + '"';
  },

  /*
   * dt: the column name
   * dd: the data in the column
   * ip: return itemprop HTML attribute
   */
  format:function(fmt){
    var out='';
    this.dts().forEach(function(dt){
      out+=fmt
           .replace(/\{dt\}/g,dt)
           .replace(/\{dd\}/g,this.dd(dt))
           .replace(/\{ip\}/g,this.itemprop(dt));
    },this);
    return out;
  },

  // returns a bunch-o dt and dd tags, but not the sourounding dl tag.
  dl:function(){
    return this.format('<dt>{dt}</dt><dd>{dd}</dd>');
  },

  th:function(){
    return '<tr>' + this.format('<th>{dt}</th>') + '</tr>';
  },
  td:function(){
    return '<tr itemscope itemtype="' + this.type() + '">'
         + this.format('<td{ip}>{dd}</td>') + '</tr>';
  },

  panel:function(){
    return this.format
    ('<div class="panel panel-default">' +
     '<div class="panel-heading">{dt}</div>' +
     '<div class="panel-body">{dd}</div>'    +
     '</div>');
  },


  /*
   * Content that needs to be wrapped around something like:
   *   <div class="panel-group" id="panel_id">
   *   <div class="panel panel-default">{here}</div></div>
   */
  collapsible_panel:function(panel_id){
    return this.format
    ('<div class="panel panel-default">' +
     '<div class="panel-heading">' +
     '<h2 class="panel-title">' +
     '<a data-toggle="collapse" data-parent="#' +
     panel_id +
     'publications" href="#{dt}">{dt}' +
     '</a></h2></div>' + // panel-heading
     '<div id="{dt}" class="panel-collapse collapse' +
     '">' +
     '<div class="panel-body">{dd}</div>' +
     '</div>' + // panel-collapse
     '</div>');
  },

};


// This part is specific to home.php, if we ever need ims.js elsewhere
// it will need to be abstracted or moved there.
$(document).ready(function(){

  // Will only stay if we end up using tablesorter
  $.extend($.tablesorter.themes.bootstrap,{
    table:'',
    even:'ui-state-default',
    odd:'ui-state-default',
  });

  // check if we are already logged in or not.
  $.ajax(IMS.ajax_query({},{url:'user.php'}))
  .success(IMS.loggedin_html)
  .fail(IMS.login_html);


  // Set up select2 pubmed search.
  $("#pubmed").select2({
    minimumInputLength:3,
    formatResult:function(obj){
      var out=obj.format_item();
      //console.log(out);
      return out;
    },
    formatSelection:function(pub){
      // When we are here we have selected a pubmed paper.
      IMS.set_publication(pub); // maybe this should be in a button
      $('.ifpub').removeClass('hidden');
      return pub.format_item();
    },
    /*
    initSelection:function(e,c){
      console.log(e);
      console.log(c);
    },
     */
    ajax:IMS.ajax_query(
      function(term,page){
        return{
          limit:10,
          table:'publications',
          q:term
        }
      },{
        results:function(data){
          IMS.report_messages(data.messages);
          var out=[];
          for(var row in data.results){
            out.push(new IMS.Publication(data.results[row]));
          }
          return {results:out};
        }
      }
    ) // ajax_query
  }); // select2

  /*
   * Stuff for creating new Interactions and Participants
   */

  /*
  IMS.populate_select(IMS.Participant_role);
  IMS.populate_select(IMS.Participant_type);
   */
  IMS.populate_select(
    IMS.Interaction_type,
    {callback:IMS.Interaction_type.fieldsets}).
    change(IMS.Interaction_type.fieldsets);
  //IMS.populate_select(IMS.Quick_organism);

  $('#commit').click(function(){
    IMS.pub.commit();
  });

  $('#participant_selector .ok').click(function(){
    var i=IMS.pub.interaction;

    IMS.query(
      {participant_value:$('#quick').val(),
       participant_type_id:$('.quick_type').val(),
       table:'participants'},
      function(results){
        // need to check we only have one result.
        var ip=new IMS.Interaction_participant({
          interaction_participant_id:--i.new_id,
          interaction_id:i.primary_id(),
          participant_id:results[0].participant_id,
          participant_role_id:$('.participant_role').val(),
          interaction_participant_status:'active',
          interaction_participant_addeddate:'new'
        });
        i.participants[ip.id]=ip;
        i.participant=ip;

        var tbl=ip.$('table');
        IMS.add_row(tbl.find('thead'),tbl.find('tbody'),ip); //.click(IMS.click_participant)
        IMS.update_danger(tbl);
        tbl.trigger('update');
      });
  });


  /*
   * modify modal
   */

  $('#ontologies').on('show.bs.modal',function(e){
    var m=$(this);
    var i=IMS.pub.interaction;

    IMS.query({interaction_id:i.id,table:'interaction_ontologies'},
              function(r){
                IMS.redo_table(r,IMS.Interaction_ontology);
              });

    m.find('.interaction_id').html(i.id);
  });

}); // ready
