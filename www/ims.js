// Items that start with a capitol letter are reserved for table
// objects related to the database.
IMS={

  /*
   * First, a bunch af utilities.
   */

  // Returns the current publication_id.
  // What page publication we are currently looking at
  pub_id:null,
  publication_id:function(){
    if(!this.pub_id){
      this.pub_id=Number($('$publication_id div').text());
    }
    return this.pub_id;
  },

  // Looks up constant data from _table objects, not Table instances.
  constant:function(Table,get){
    return Table.prototype._const[get];
  },

  // Report errors, usually from the query.php script, on the log page.
  report_messages:function(messages){
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
      data:request,
      table:request.table,
      cache:true,
    };
    if(also){
      for(var key in also){
        out[key]=also[key];
      }
    }
    return out;
  },

  query_count:0,
  query:function(request,act){
    if(3>IMS.query_count){ // only 3 queries at a time
      IMS.query_count++;
      //console.log(IMS.query_count,'up');
      $.ajax(IMS.ajax_query(request,IMS.act)).done(
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

  cache:function(request,act,primary_key){
    var store=localStorage;
    switch(primary_key){
      case 'participant_id':
      store=sessionStorage;
    }
    var have=store.getItem(primary_key);
    have=(null==have)?{}:JSON.parse(have);
    if(have[request[primary_key]]){
      act([have[request[primary_key]]]);
    }else{
      IMS.query(request,function(data){
        // Hurry up and update the user feedback.
        act(data);

        // We do this again since the ajax query is asynchronous.
        have=store.getItem(primary_key);
        have=(null==have)?{}:JSON.parse(have);

        have[data[0][primary_key]]=data[0];
        store.setItem(primary_key,JSON.stringify(have));
      });
    }
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
    // clear some thingsfrom the last publication
    $("#participants").html('<thead/><tbody/>');
    $(".participant-count").html('');

    IMS.pub_id=pub.primary_id();
    $("#publication").html(pub.select('publication_abstract'));

    IMS.query({publication_id:this.pub_id,table:'interactions'},
              IMS.update_interactions);
  },

  // try to get an active object from a HTML tag burried in a
  // itemscope.
  active:function(tag){
    var item=tag.parentsUntil('tr[itemscope]').parent();
    var pk=IMS[item.attr('itemtype')]
           ._active[item.find('[itemprop=primary-key]').text()];
    return pk;
  },

  update_danger:function(tbl){
    tbl.find('.bg-danger').each(function(){
      var tag=$(this);
      var prop=tag.parent().attr('itemprop');

      // Not sure how portable this is
      var Table=IMS[prop.charAt(0).toUpperCase()+prop.slice(1)];

      if(Table){
        // Stuff we can figure out without actually accessing the
        // object in scope.
        var primary_key=IMS.constant(Table,'primary_key');
        var request={table:IMS.constant(Table,'table')};
        request[primary_key]=tag.text();
        IMS.cache(request,function(raw){
          tag.replaceWith(new Table(raw[0]).html());
        },primary_key);
      }
      /*
      else{
        // Here we gotta get the object first.
        var i=IMS.active(tag);
        i.prop(prop,tag);
        tag.html('Fetching ' + prop + '?');
      }
       */

    });
  },

  // Abstracted was to dump results from query.php into an HTML table.
  update_table:function(results,Table,other){
    $(IMS.constant(Table,'count_class')).html('('+results.length+')');

    var tbl=$(IMS.constant(Table,'table_id'));
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


    // Populate the table with results.
    for(var row in results){
      var i=new Table(results[row]);
      if(0==row){
        thead.append(i.th());
      }
      tbody.append(i.td());
    }

    // So we can use some CSS to align the numbers right but still
    // keep them, more or less, left.
    tbody
    .find('.primary-key')
    .wrapInner('<span></span>');

    // We have something else to do!
    if(other){
      other(tbody);
    }

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
    this.update_danger(tbl)

    // Return the tbody so we can add events, et al.
    return tbody;
  },

  _interaction_tr:null, // selected interaction in the table
  update_interactions:function(results){
    IMS.Interaction._active={};
    IMS.update_table(results,IMS.Interaction,function(tbody){
      tbody.find('tr')
      .click(function(){
        var tag=$(this);
        //tag.parent().find('.active').removeClass('active');
        if(IMS._interaction_tr){
          IMS._interaction_tr.removeClass('active');
        }
        IMS._interaction_tr=tag;
        tag.addClass('active');
        var interaction_id=tag.find('[itemprop=primary-key]').text();
        IMS.query({interaction_id:interaction_id,
                   table:'interaction_participants'},
                  IMS.update_participants);
      });
    });
  },

  // Perhaps this should be update interaction_participants?
  update_participants:function(results){
    IMS.update_table(results,IMS.Interaction_participant);
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
  _table:function(){
    // Here to make select2 happy
    this.__defineGetter__('id',function(){
      return this.primary_id();
    })
  }
}


IMS._table.prototype={
  // Returns the SQL table.
  table:function(){
    return this._const.table;
  },
  type:function(){
    table=this.table();
    return table.charAt(0).toUpperCase()+table.slice(1);
  },
  // returns the column name that contains the primary_id of the
  // table.
  primary_col:function(){
    return this._const.primary_key;
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

  // Return a list of definition term names, that then can be fed to
  // the dt function.
  dts:function(){
    return Object.keys(this.data);
  },
  dd:function(dt){
    if(this.data[dt]){
      return this.data[dt];
    }
    return '<span class="bg-danger">'+this.data[dt+'_id']+'</span>';
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
      dd=this.dd(dt);
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
    if(dt==this._const.primary_key){
      return ' itemprop="primary-key"';
    }else if(!this.data[dt]){
      return ' itemprop="' + dt + '"';
    }
    return '';
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
     '<div class="panel-body">{dd}</div>'+
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

  // should bury this in IMS.* somehow
  $("#pubmed").select2({
    minimumInputLength:3,
    formatResult:function(obj){
      return obj.format_item();
    },
    formatSelection:function(pub){
      IMS.set_publication(pub); // maybe this should be in a button
      return pub.format_item();
    },
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
   * Here we populate the pull down box on the ID Conersion page.
   */
  var sel=$('#id-from>select,#id-to>select');
  IMS.query(
    {table:'quick_identifier_types'},
    function(results){
      for(var row in results){
        var result=new IMS.Quick_identifier_type(results[row]);
        sel.append(result.option('ENTREZ_GENE'));
      }
    });

  /*
   * Here is what happends when you actually click to convert IDs of a
   * document.
   */

  var bg2id=function(results){
    $('#id-to>dl').html('<dt>IDs Returned</dt><dd>'+results.length+'</dd>');
    var to=$('#id-to>textarea');
    for(var row in results){
      var result=new IMS.Quick_identifier(results[row]);
      to.append(result+"\n");
    }
  }
  var from2bg=function(results){
    $('#id-to>textarea').html('');
    var bgid=[];
    for(var row in results){
      result=results[row];
      bgid.push(result.gene_id);
    }
    IMS.query(
      {table:'quick_identifiers',
       quick_identifier_type:$('#id-to>select').val(),
       gene_id:bgid.join('|')},bg2id);
  };

  $('#conv')
  .click(function(){
    var from=$('#id-from>textarea').val().trim().split(/\W/);
    $('#id-from>dl').html('<dt>IDs Detected</dt><dd>'+from.length+'</dd>');
    from=from.join('|');
    IMS.query(
      {table:'quick_identifiers',
       quick_identifier_type:$('#id-from>select').val(),
       quick_identifier_value:from},from2bg);
  });

}); // ready
