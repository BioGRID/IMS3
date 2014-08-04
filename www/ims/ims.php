<?php namespace IMS;
require_once('pubmed.php');

// Hopefully in the RPM we will always have version.php, but in dev
// it's ok if we don't.
if(stream_resolve_include_path('version.php')){
  include_once('version.php');
}else{
  DEFINE("IMS3_VERSION","???");
}



global $errors_reported;
$errors_reported=FALSE;
global $errors;
$errors=[];
function divert_errors(){
  register_shutdown_function(function(){
      global $errors_reported;
      if(!$errors_reported){
	print json_encode(['messages'=>[error_get_last()]]);
      }
    });
  set_error_handler(function($errno,$errstr,$filename,$linenum,$vars){
      global $errors;
      // hopefully this is the same as error_get_last() produces.
      $errors[]=
	[
	 'type'=>$errno,
	 'message'=>htmlentities($errstr),
	 'file'=>$filename,
	 'line'=>$linenum
	 ];
      return FALSE;
    },E_ALL);
  error_reporting(0);
  #trigger_error("Messaging On",E_USER_NOTICE);
}

function int($val){
  return (int)$val;
}


class config
{
  private $path;
  function __construct($json){
    $saved_include_path=get_include_path();
    set_include_path('..:/etc');
    $this->config=json_decode(file_get_contents($json,FILE_USE_INCLUDE_PATH));
    set_include_path($saved_include_path);
  }

  public $pdos=[];
  function pdo($db){
    if(!isset($this->pdos[$db])){
      $c=$this->config->dbs->$db;
      $this->pdos[$db]=new \PDO('mysql:host=localhost;dbname='.$c->db,
			      $c->user,$c->passwd);
    }
    return $this->pdos[$db];
  }

  function title(){
    return $this->config->title;
  }

  function version(){
    return IMS3_VERSION;
  }

  function html_head(){
    $out=[];
    foreach($this->config->css as $css){
      $out[]=sprintf('<link href="%s" rel="stylesheet">',$css);
    }
    foreach($this->config->js as $js){
      $out[]=sprintf('<script src="%s"></script>',$js);
    }
    return join("\n",$out);
  }

  function now(){
    return date("c");
  }
  function pubmed_update($cur){
    if(NULL==$cur){
      return TRUE;
    }
    return date($cur) <= date($this->config->pubmed_update);
  }
}


class _Table
{
  const DB='ims'; // this name of the database as specified in the
                  // ims.json file.

  // consts to be defined by children classes:
  const TABLE=null;          // The of the SQL table
  const PRIMARY_KEY=null;    // The primary key of the SQL table
  const STATUS_COLUMN=null;  // The status column of the SQL table
  const DEFAULT_STATUS=null; // The default status of the SQL table
  const ORDER_BY=null;       // If the table needs to be sorted

  public function __construct($cfg,$qs){
    $this->cfg=$cfg;
    $this->qs=$qs;
  }

  public function pdo(){
    $c=get_called_class();
    return $this->cfg->pdo($c::DB);
  }


  public function _ineq($tainted,$qm){
    $vs=explode('|',$tainted);
    if(1==count($vs)){
      return '='.$qm($tainted);
    }
    $in=[];
    foreach($vs as $v){
      $in[]=$qm($v);
    }
    return ' IN('.implode(',',$in).')';
  }

  # Currently only being used by Publication whet making queries to
  # PubMed
  public function update($pk,$to){
    $c=get_called_class();
    $dbh=$this->pdo();
    $sql='UPDATE ' . $c::TABLE . ' SET ';
    $first=TRUE;
    foreach($to as $col=>$data){
      if($first){
	$first=FALSE;
      }else{
	$sql.=',';
      }
      $sql.=$col."=".$dbh->quote($data);
    }
    $sql.=' WHERE '.$c::PRIMARY_KEY.'='.$pk;

    $s=$dbh->prepare($sql);
    $s->execute();
  }

  public function _where(){
    $c=get_called_class();
    $dbh=$this->pdo();
    $where=[];
    foreach($this->qs as $k=>$v){
      switch($k){
      case '_':
      case 'limit':
	break;
      case 'q':
	$where[]=$c::SEARCH_COLUMN.' LIKE '.$dbh->quote($v.'%');
	break;
      case 'status':
	if($c::STATUS_COLUMN){
	  $where[]=$c::STATUS_COLUMN."=".$dbh->quote($v);
	}else{
	  trigger_error('Table '.$this->table().' has no status column.');
	}
	break;
      case $c::PRIMARY_KEY:
      case 'publication_id':
      case 'interaction_id':
	$where[]=$k.$this->_ineq($v,function($x){
	    return (int)$x;
	  });
      break;
      default:
	$where[]=$k.$this->_ineq($v,function($x){
	    $dbh=$this->pdo();
	    return $dbh->quote($x);
	      });
      }
    }
    return $where;
  }
  

  public function status_match(){
    $c=get_called_class();
    if($c::DEFAULT_STATUS){
      if(!isset($this->qs['status'])){
	$this->qs['status']=$c::DEFAULT_STATUS;
      }
    }
  }

  public function table(){
    $c=get_called_class();
    return $c::TABLE;
  }

  public function sql(){
    $c=get_called_class();
    $sql='SELECT * FROM ' . $c::TABLE;
    $where=$this->_where();
    $this->status_match();

    if(0<count($where)){
      $sql.=' WHERE '.implode(' AND ',$where);
    }
    
    if($c::ORDER_BY){
      $sql.=' ORDER BY '.$c::ORDER_BY;
    }

    if(isset($this->qs['limit'])){
      $limit=(int)$this->qs['limit'];
      $sql.=" LIMIT $limit ";
    }

    return $sql;
  }

  public function query(){
    $dbh=$this->pdo();
    $sql=$this->sql();
    $this->statement=$dbh->prepare($sql);
    $out=$this->statement->execute();
    if(!$out){
      trigger_error($sql . ' failed.');
    }
    return $out;
  }

  public function fetch(){
    return $this->statement->fetch(\PDO::FETCH_ASSOC);
  }

  public function message($row,$msg){
    $c=get_called_class();
    return sprintf('Where %s=%d %s',$c::PRIMARY_KEY,$row[$c::PRIMARY_KEY],
		   $msg);
  }
} // _Table

class _Quick extends _Table{
  const DB='quick';
}

class Quick_identifiers extends _Quick
{
  const TABLE='quick_identifiers';
  const PRIMARY_KEY='gene_id'; // not unique
}

class Quick_identifier_types extends _Quick
{
  const TABLE='quick_identifiers';
  # The _where() function assumes the PRIMARY_KEY's value is an
  # integer, but as we overide the the sql() function we skip that
  # part.
  const PRIMARY_KEY='quick_identifier_type';
  public function sql(){
    $c=get_called_class();
    return sprintf("SELECT DISTINCT %s FROM %s",$c::PRIMARY_KEY,$c::TABLE);
  }
}

class Interactions extends _Table
{
  const TABLE='interactions';
  const PRIMARY_KEY='interaction_id';
  const STATUS_COLUMN='interaction_status';
  const DEFAULT_STATUS='normal';

  public function fetch(){
    $out=current($this->data);
    next($this->data);
    return $out;
  }

  public function query(){
    $r=parent::query();
    $this->data=[];
    while($v=$this->statement->fetch(\PDO::FETCH_ASSOC)){
      $ih=new Interaction_history
	($this->cfg,['interaction_id'=>$v['interaction_id'],'limit'=>1]);
      $ih->query();
      $mt=$ih->fetch();
      $v['modification_type']=$mt?$mt['modification_type']:false;
      $this->data[]=$v;
    }
    reset($this->data);
    return $this->data;
  }

}

class Interaction_history extends _Table
{
  const TABLE='interaction_history';
  const PRIMARY_KEY='interaction_history_id';
  const ORDER_BY='interaction_history_date DESC';
}

class Interaction_sources extends _Table
{
  const TABLE='interaction_sources';
  const PRIMARY_KEY='interaction_source_id';
  const STATUS_COLUMN='interaction_source_status';
  const DEFAULT_STATUS='active';
}

class Interaction_types extends _Table
{
  const TABLE='interaction_types';
  const PRIMARY_KEY='interaction_type_id';
  const STATUS_COLUMN='interaction_type_status';
  const DEFAULT_STATUS='active';
}

class Interaction_participants extends _Table
{
  const TABLE='interaction_participants';
  const PRIMARY_KEY='interaction_participant_id';
  const STATUS_COLUMN='interaction_participant_status';
  const DEFAULT_STATUS='active';
}

class Participant_roles extends _Table
{
  const TABLE='participant_roles';
  const PRIMARY_KEY='participant_role_id';
  const STATUS_COLUMN='participant_role_status';
  const DEFAULT_STATUS='active';
}

class Participants extends _Table
{
  const TABLE='participants';
  const PRIMARY_KEY='participant_id';
  const STATUS_COLUMN='participant_status';
  const DEFAULT_STATUS='active';
}

class Publications extends _Table
{
  const TABLE='publications';
  const PRIMARY_KEY='publication_id';
  const STATUS_COLUMN='publication_status';
  const DEFAULT_STATUS='active';
  const SEARCH_COLUMN='publication_pubmed_id';

  public function fetch(){
    $out=$this->statement->fetch(\PDO::FETCH_ASSOC);
    if(!$out){
      return $out;
    }
    if($this->cfg->pubmed_update($out['publication_lastupdated'])){
      $pm=new \PubMedID($out[self::SEARCH_COLUMN]);
      trigger_error($this->message($out,"fetched MEDLINE for PMID:".$out[self::SEARCH_COLUMN]),E_USER_NOTICE);
      $date=$pm->date();
      if(NULL==$date){
	trigger_error($this->message($out,"unknown date format"),E_USER_WARNING);
      }
      $this->update
	($out[self::PRIMARY_KEY],
	 [
	 'publication_article_title'=>$pm->article_title(),
	 'publication_abstract'=>$pm->abs(),
	 'publication_author_short'=>$pm->author_short(),
	 'publication_author_full'=>$pm->author_full(),
	 'publication_volume'=>$pm->volume(),
	 'publication_issue'=>$pm->issue(),
	 'publication_date'=>$date,
	 'publication_journal'=>$pm->journal(),
	 'publication_pagination'=>$pm->pagination(),
	 'publication_affiliation'=>$pm->affiliation(),
	 'publication_meshterms'=>$pm->meshterms(),
	 'publication_lastupdated'=>$this->cfg->now()
	 ]);
      $updated=new Publications
	($this->cfg,
	 [
	  'publication_id'=>$out['publication_id'],
	  ]);
      $updated->query();
      return $updated->statement->fetch(\PDO::FETCH_ASSOC);
    }else if(0==(int)$out['publication_date']){
      trigger_error
	($this->message
	 ($out,'publication_date='.$out['publication_date']),
	 E_USER_WARNING);
    }
    return $out;
  }
}

function table_factory($cfg,$qs)
/* Will return an object for a given table. Or Null if not a valid
   table. */
{
  $table=$qs['table'];
  unset($qs['table']);

  // We don't need breaks because we are always returning.
  switch($table){
  case 'interactions':
    return new Interactions($cfg,$qs);
  case 'interaction_history':
    return new Interaction_history($cfg,$qs);
  case 'interaction_participants':
    return new Interaction_participants($cfg,$qs);
  case 'participant_roles':
    return new Participant_roles($cfg,$qs);
  case 'interaction_sources':
    return new Interaction_sources($cfg,$qs);
  case 'interaction_types':
    return new Interaction_types($cfg,$qs);
  case 'participants':
    return new Participants($cfg,$qs);
  case 'publications':
    return new Publications($cfg,$qs);
  case 'quick_identifiers':
    return new Quick_identifiers($cfg,$qs);
  case 'quick_identifier_types':
    return new Quick_identifier_types($cfg,$qs);
  }
  trigger_error("Can't access requested data",E_USER_ERROR);
  return NULL;
}


function messages2json(){
  global $errors,$errors_reported;
  $errors_reported=TRUE;
  return json_encode($errors);
}
/* Print PDOstatement as JSON. */
function pdo2json($r){
  global $errors;
  $first=TRUE;
  print '{"results":[';
  while($v=$r->fetch()){
    if($first){
      $first=FALSE;
    }else{
      print ',';
    }
    print json_encode($v);
  }

  print '],"messages":' . messages2json() . '}';
}
