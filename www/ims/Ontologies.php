<?php namespace IMS;

class Ontologies extends _Table
{
  const TABLE='ontologies';
  const PRIMARY_KEY='ontology_id';
  const STATUS_COLUMN='ontology_status';
  const DEFAULT_STATUS='active';

  protected function radio_term($ot){
    $name=$this->row['ontology_name'];
    //print "<h1>$name</h1>";
    return sprintf('<label><input type="radio" name="%s" value="%s">%s</label>',
		   $name,
		   $ot['ontology_term_id'],
		   $ot['ontology_term_name']);
  }

  // tree to table:
  //  $kids: output ontology_terms::tree
  protected function t2t($x,$kids,$n,&$out){
    $ys=$kids[$x];
    foreach($ys as $ot){
      $y=$ot['ontology_term_id'];
      
      $kidsp=array_key_exists($y,$kids);
      if($kidsp){
	$html=$ot['ontology_term_name'];
      }else{
	$html=$this->radio_term($ot);
      }

      if(array_key_exists($n,$out)){
	array_push($out[$n],$html);
      }else{
	$out[$n]=[$html];
      }
      
      // 
      if($kidsp){
	$n=$this->t2t($y,$kids,$n,$out);
	$n++;
      }
    }
    return $n;
  }


  // Don't use this for sets with large numbers of terms, link most of
  // them
  public function fieldset_radio_html(){
    $this->query();
    $o=$this->fetch_only_one('fieldset_radio_html');
    $terms=new Ontology_terms($this->cfg,['ontology_id'=>$o['ontology_id']]);
    $tree=$terms->tree();

    $trs=[];
    if(array_key_exists('root',$tree)){
      $root_id=$tree['root']['ontology_term_id'];
      
      $rows=[];
      $this->t2t($root_id,$tree,0,$rows);

      $row_count=0;
      foreach($rows as $row){
	if(count($row)>$row_count){
	  $row_count=count($row);
	}
      }

      for($i=0;$i < $row_count;$i++){
	$tds=[];
	foreach(array_keys($rows) as $j){
	  if(array_key_exists($i,$rows[$j])){
	    array_push($tds,'<td>' . $rows[$j][$i] . '</td>');
	  }else{
	    array_push($tds,'<td></td>');
	  }
	}
	array_push($trs,'<tr>' . implode('',$tds) . '</tr>');
      }
      
    }else{
      $trs=[];
      foreach($tree as $leaf){
	array_push($trs,'<tr><td>' . $this->radio_term($leaf) . '</tr></td>');
      }
    }

    return '<fieldset class="ontology"><legend>' . $o['ontology_name'] . '</legend><table border="1px">'
      . implode('',$trs) . '</table></fieldset>';
  }

  
}
