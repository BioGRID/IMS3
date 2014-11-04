<?php
require_once('ims/ims.php');
#IMS\divert_errors();
header('Contest-type: text/plain');
$cfg=new IMS\config('ims.json');

# convert gene_id to participant_id
function id_gene2part($gene_id,$cfg){
  $qs=
    [
     'participant_type_id' => 1,
     'participant_value'   => $gene_id,
     ];

  $p=new IMS\Participants($cfg,$qs);
  $p->query();
  $v=$p->fetch();
  return $v['participant_id'];
}


# Each key in $_POST should contain a list.  Item zero being an
# organism_id number, the rest being quick_identifier_value entries.

$ok=[];   // list of gene_id=>$value
$miss=[]; // list of missing $value items
$mult=[]; // list of $value items matchi multiple gene_id
foreach($_POST as $col => $values){
  $ok[$col]=[];
  $org_id=array_shift($values);
  foreach($values as $value){
    $qs=
      [
       'organism_id'            => $org_id,
       'quick_identifier_value' => $value,
       ];
    $qit=new IMS\Quick_identifiers($cfg,$qs);
    $qit->query();

    // Lets see what we got
    $got=[];
    while($v=$qit->fetch()){
      array_push($got,$v['gene_id']);
    }
    $got=array_unique($got);

    switch(count($got)){
    case 0:
      array_push($miss,$value);
      break;
    case 1:
      array_push($ok[$col],[id_gene2part($got[0],$cfg) => $value]);
      break;
    default:
      array_push($mult,[$value => $got]);
    }
  }
}

// make a report for output
$out=[];
if(0 != count($ok)){
  $out['ok']=$ok;
}
if(0 != count($miss)){
  $out['missing']=$miss;
}
if(0 != count($mult)){
  $out['multiple']=$mult;
}

print json_encode($out);
