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

  _table:function(data){
    this.data=data;

    // Here to make select2 happy
    this.__defineGetter__('id',function(){
      return this.primary_id();
    })
  },

  report_messages:function(messages){
    $('.message-count').html('('+messages.length+')');
    list=$('#messages').html('');
    for(var row in messages){
      msg=messages[row];
      type=IMS.php_error(msg['type']);
      html='<p class="error ' + (type?type:'E_UNKNOWN') + '">' +
        '<span class="type">' + (type?type:'E_UNKNOWN('+msg['type']+')') + '</span>: ' +
        '<span class="message">' + msg['message'] + '</span> in ' +
        '<span class="file">' + msg['file'] + '</span> ' +
        'on line ' + msg['line'] + '</p>';
      list.append(html);
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

  Publication:function(data){
    this.data=data;

    // Move this up to IMS._table if we need to use select2 for a
    // different items buth publication.
    this.__defineGetter__('text',function(){
      return this.pmid();
    });
  },

  Interaction:function(data){
    this.data=data;
  },


  Interaction_source:function(data){

  },


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
  }
}


IMS._table.prototype={
  primary_id:function(){
    return this.data[this._cols.primary_key];
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
  }

};


IMS.Interaction.prototype=new IMS._table();
IMS.Interaction.prototype._cols={
  primary_key:'interaction_id'
};
IMS.Interaction.prototype.dts=function(){
  return [
    'interaction_id',
    //'participant_hash',
    //'publication_id',
    'interaction_type_id',
    'interaction_status',
    //'interaction_source_id',
    'interaction_source',
  ];
}
IMS.Interaction.prototype.dd=function(dt){
  switch(dt){
    case 'interaction_source': return this.interaction_source();
  }
  return this.data[dt];
}


// Need to abstract this
IMS.Interaction.prototype.interaction_source=function(){
  if(!localStorage.getItem('interaction_source')){
    ajax=$.ajax({
      async:false,
      type:'GET',
      url:'query.php',
      dataType:'json',
      data:{table:'interaction_sources'}
    }).done
    (function(data){
      IMS.report_messages(data.messages);
           if(data.results){
             store_me={};

             foo=function(row){
               store_me[row.interaction_source_id]=row.interaction_source_name;
             }
             data.results.forEach(foo);
             localStorage.setItem('interaction_source',
                                  JSON.stringify(store_me));
             }
    });
  }
  return JSON.parse(localStorage.getItem('interaction_source'))[this.data.interaction_source_id];
}



IMS.Publication.prototype=new IMS._table();
IMS.Publication.prototype._cols={
  primary_key:'publication_id'
}
IMS.Publication.prototype.format_item=function(){
  return this.data.publication_pubmed_id + ' - ' +
    this.data.publication_article_title;
}
IMS.Publication.prototype.pmid=function(){
  return this.data['publication_pubmed_id'];
}


$(document).ready(function(){

  // Need to bury this in IMS.* somehow
  $("#pubmed").select2({
    minimumInputLength:1,
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