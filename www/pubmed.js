function bla(item){
  return '<li>' + item.publication_pubmed_id + ' -- ' + item.publication_article_title + '</li>';
}

/*
$(document).ready(function(){
  $("#pubmed").tokenInput('query.php?table=publications',{
    tokenValue:'publication_id',
    propertyToSearch:'publication_pubmed_id',
    hintText:'Enter PubMed ID',
    tokenFormatter:bla,
    resultsFormatter:bla,
  });
});
*/

$(document).ready(function(){
  $("#pubmed").select2({
    minimumInputLength:1,
    formatResult:function(object){
      console.log(object);
      return object.text + ' - ' + object.foo.publication_article_title;
    },
    ajax:{
      url:'query.php',
      dataType:'json',
      results:function(data,page){
        out=[];
        for(var row in data){
          out.push({
            id:data[row].publication_id,
            text:data[row].publication_pubmed_id,
            foo:data[row]
          });
        }
        return {results:out};
      },
      data:function(term,page){
        return{
          table:'publications',
          q:term,
        }
      }
    }
  });

});