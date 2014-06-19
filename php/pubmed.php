<?php

// Used to fetch data from PubMed
class PubMedID
{
  public function __construct($pmid){
    $this->pmid=(int)$pmid;

    if(0==$this->pmid){
      return null;
    }

    $this->url='https://www.ncbi.nlm.nih.gov/pubmed/?' .
      'report=medline&format=text&term=' . $this->pmid;
    $this->data=[];

    $tag='';
    $data='';

    # Fetch MEDLINE data and split it into lines
    foreach(explode("\n",file_get_contents($this->url)) as $line){
      if('<'!=$line[0]){
	if('-'==$line[4]){
	  if(''!=$tag){
	    $this->data[$tag][]=$data;
	  }

	  $ml=explode('-',$line,2);
	  $tag=trim($ml[0]);
	  $data=trim($ml[1]);
	}else{
	  $data.=' '.trim($line);
	}
      }
    }    
  }

  /* See:
   *  http://www.ncbi.nlm.nih.gov/books/NBK3827/table/pubmedhelp.T44/?report=objectonly
   * for valid options for the $tag argument.
   */
  public function medline($tag){
    if(isset($this->data[$tag])){
      return $this->data[$tag];
    }
    return NULL;
  }

  // This point on is where the specific BioGRID format items go.
  public static function sanitize($string){
    return htmlspecialchars($string); // make this ASCII only characters
  }


  public function article_title(){
    return self::sanitize($this->medline('TI')[0]);
  }

  public function abs(){
    // Can't use abstracte() as that is a PHP reserved word.
    return self::sanitize($this->medline('AB')[0]);
  }

  public function author_short(){
    return self::sanitize($this->medline('AU')[0]);
  }

  public function author_full(){
    return self::sanitize($this->medline('FAU')[0]);
  }

  public function volume(){
    return $this->medline('VI')[0];
  }

  public function issue(){
    return $this->medline('IP')[0];
  }


  // Parse 
  public function date(){
    $parse_me=$this->medline('DP')[0];

    $tries=['Y M j|','Y M|','Y M#???|','Y|'];
    $date=FALSE;
    while(!$date and $tries){
      $try=array_shift($tries);
      $date=DateTime::createFromFormat($try,$parse_me);
    }
    if(!$date){
      trigger_error("Can't parse: " . $parse_me,E_USER_WARNING);
      return NULL;
    }

    $out=$date->format('Y-m-d');
    trigger_error("Parsed '".$parse_me."' to '".$out."'");
    return $out;
  }

  public function journal(){
    return self::sanitize($this->medline('JT')[0]);
  }

  public function pagination(){
    return $this->medline('PG')[0];
  }

  public function affiliation(){
    return self::sanitize($this->medline('AD')[0]);
  }

  public function meshterms(){
    return self::sanitize(implode('|',$this->medline('MH')));
  }

}
