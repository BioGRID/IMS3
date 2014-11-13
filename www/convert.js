$(document).ready(function(){

  /*
   * ID conversion page stuff
   */

  // Here we populate the pull down box on the ID Conersion page.
  var sel=$('#id-from>select,#id-to>select');
  IMS.query(
    {table:'quick_identifier_types'},
    function(results){
      for(var row in results){
        var result=new IMS.Quick_identifier_type(results[row]);
        sel.append(result.option('ENTREZ_GENE'));
      }
    });

  // Here is what happends when you actually click to convert IDs of a
  // document.
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

});