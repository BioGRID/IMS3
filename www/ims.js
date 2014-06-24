// Items that start with a capitol letter are reserved for table
// objects related to the database.
IMS={
  pub_id:null,

  update_publication:function(pub){

    that=this;
    this.pub_id=pub.primary_id();
    $("#publication div").html(pub.collapsible_panel('publication'));

    ajax=$.ajax({
      type:'GET',
      url:'query.php',
      dataType:'json',
      data:{publication_id:this.pub_id,
            table:'interactions'},
    }).done(this.update_interactions);



  },

  update_interactions:function(raw){
    that.report_messages(raw.messages);
    $('.interaction_count').html('('+raw.results.length+')');
    tbl=$('#interactions').html('');
    for(var row in raw.results){
      i=new IMS.Interaction(raw.results[row]);
      if(0==row){
        tbl.append(i.th());
      }
      tbl.append(i.td());
    }

  },

  report_messages:function(messages){
    // Add the number of new messages to the current message count.
    mc=$('.message-count');
    count=Number(mc.text());
    count+=messages.length;
    mc.text(count);

    // prepend new messages to list
    list=$('#messages');
    for(var row in messages){
      msg=messages[row];
      type=IMS.php_error(msg['type']);
      html='<p class="error ' + (type?type:'E_UNKNOWN') + '">' +
        '<span class="type">' + (type?type:'E_UNKNOWN('+msg['type']+')') + '</span>: ' +
        '<span class="message">' + msg['message'] + '</span> in ' +
        '<span class="file">' + msg['file'] + '</span> ' +
        'on line ' + msg['line'] + '</p>';
      list.prepend(html);
    }
  },

  /*
   * Returns the current publication_id.
   */
  publication_id:function(){
    if(!this.pub_id){
      this.pub_id=Number($('$publication_id div').text());
    }
    return this.pub_id;
  },



  /*
   * Returns PHP error codes as text.
   */
  php_error:function(errno){
    switch(errno){
      case     1:return 'E_ERROR';
      case     2:return 'E_WARNING';
      case     4:return 'E_PARSE';
      case     8:return 'E_NOTICE';
      case    16:return 'E_CORE_ERROR';
      case    32:return 'E_CORE_WARNING';
      case    64:return 'E_COMPILE_ERROR';
      case   128:return 'E_COMPILE_WARNING';
      case   256:return 'E_USER_ERROR';
      case   512:return 'E_USER_WARNING';
      case  1024:return 'E_USER_NOTICE';
      case  2048:return 'E_STRICT';
      case  4096:return 'E_RECOVERABLE_ERROR';
      case  8192:return 'E_DEPRECATED';
      case 16384:return 'E_USER_DEPRECATED';
      case 30719:return 'E_ALL';
    }
    return false;
  },


  // prototype for this defined below
  _table:function(data){
    this.data=data;

    // Here to make select2 happy
    this.__defineGetter__('id',function(){
      return this.primary_id();
    })
  }
}


IMS._table.prototype={
  primary_col:function(){
    return this._cols.primary_key;
  },
  primary_id:function(){
    return this.data[this.primary_col()];
  },

  // Returns HTML suitable for inlined usage.
  html:function(){
    return this.primary_col()+'='+this.primary_id();
  },

  // return a list of definition term names, that then can be fed to
  // the dt function.
  dts:function(){
    return Object.keys(this.data);
  },
  dd:function(dt){
    return this.data[dt];
  },

  format:function(fmt){
    out='';
    this.dts().forEach(function(dt){
      out+=fmt
           .replace(/\{dt\}/g,dt)
           .replace(/\{dd\}/g,this.dd(dt));
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
    return '<tr>' + this.format('<td>{dd}</td>') + '</tr>';
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

  cache:function(col){
    Table=IMS[col[0].toUpperCase() + col.substr(1)];
    pk=Table.prototype._cols.primary_key;
    pkv=this.data[col+'_id'];

    ls=localStorage.getItem(col);
    ls              =
      (null==ls)    ?
      {}            :
      JSON.parse(ls);
    if(undefined==ls[pkv]){
      ls[pkv]=this._cache(Table,pk,pkv);
      localStorage.setItem(col,JSON.stringify(ls))
    }
    return new Table(ls[pkv]);
  },
  _cache:function(Table,pk,pkv){
    data={table:Table.prototype._table};
    data[pk]=pkv;
    $.ajax({
      async:false,
      type:'GET',
      url:'query.php',
      dataType:'json',
      data:data
    }).done(function(data){
      IMS.report_messages(data.messages);
      // As we specified a primary key we should only ever get one
      // result.
      out=data.results[0];
    });

    return out;
  },



};




// This part is specific to home.php, if we ever need ims.js elsewhere
// it will need to be abstracted or moved there.
$(document).ready(function(){

  // should bury this in IMS.* somehow
  $("#pubmed").select2({
    minimumInputLength:3,
    formatResult:function(obj){
      return obj.format_item();
    },
    formatSelection:function(obj){
      IMS.update_publication(obj); // maybe this should be in a button
      return obj.format_item();
    },
    ajax:{
      url:'query.php',
      dataType:'json',
      results:function(data){
        IMS.report_messages(data.messages);
        out=[];
        for(var row in data.results){
          out.push(new IMS.Publication(data.results[row]));
        }
        return {results:out};
      },
      data:function(term,page){
        return{
          table:'publications',
          q:term
        }
      }
    }
  });
});