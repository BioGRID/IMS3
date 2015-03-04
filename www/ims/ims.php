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

  function schema($db){
    return $this->config->dbs->$db->schema;
  }

  public $pdos=[];
  function pdo($db){
    if(!isset($this->pdos[$db])){
      $c=$this->config->dbs->$db;
      $this->pdos[$db]=new \PDO('mysql:host=localhost;dbname='.$c->schema,
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

  function expires(){
    return time()+$this->config->expires;
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

  function user($user_name){
    $user=new User($this,['user_name'=>$user_name]);
    $user->query();
    return $user;
  }
  function verify_user(){
    // as user_name is unique their can be only one
    $user=$this->user($_COOKIE['name'])->fetch();
    if($_COOKIE['auth']==$user['user_cookie']){
      return $user;
    }
    return null;
  }
  
  function verify_user_or_die(){
    $user=$this->verify_user();
    if(!$user){
      header('HTTP/1.1 403 Forbidden');
      exit(1);
    }
    return $user;
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

  public function schema(){
    $c=get_called_class();
    return $this->cfg->schema($c::DB);
  }

  public function pdo(){
    $c=get_called_class();
    return $this->cfg->pdo($c::DB);
  }

  public function status_options(){
    $c=get_called_class();
    $dbh=$this->pdo();
    $sql='SELECT COLUMN_TYPE FROM information_schema.columns '
      . "WHERE table_name='" . $c::TABLE . "' "
      . "AND column_name='" . $c::STATUS_COLUMN . "' "
      . "AND table_schema='" . $this->schema() . "'";
    $s=$dbh->prepare($sql);
    $s->execute();
    $v=$s->fetch();
    $out=explode(',',str_replace("'",'',ltrim(rtrim($v[0],')'),'enum(')));
    print "\n";

    return $out;
  }
  

  protected function _ineq($tainted,$qm){
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

  # Modify a table, use with caution.
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

  protected function _where(){
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

  protected function columns(){
    return '*';
  }

  // this is seperated to allow overloding, as it is in
  // Project_publications
  public function _select(){
    $c=get_called_class();
    return 'SELECT ' . $c::columns() . ' FROM ' . $c::TABLE;
  }

  public function count(){
    $c=get_called_class();
    $sql='SELECT COUNT(*)FROM ' . $c::TABLE . ' WHERE ' . implode(' AND ',$this->_where());
    $dbh=$this->pdo();
    $s=$dbh->prepare($sql);
    $s->execute();
    $g=$s->fetch(\PDO::FETCH_NUM);
    return $g[0];
  }

  public function sql(){
    $c=get_called_class();
    $sql=$this->_select();
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
    $out=$this->statement->fetch(\PDO::FETCH_ASSOC);
    $this->row=$out;
    return $out;
  }

  public function id(){
    $c=get_called_class();
    return $this->row[$c::PRIMARY_KEY];
  }

  public function ids(){
    $out=[];
    $this->query();
    while($this->fetch()){
      array_push($out,$this->id());
    }
    return $out;
  }

  # Fetch one, but zero is ok too.
  public function fetch_one($error_hist){
    $c=get_called_class();
    $got=[];

    // Uniqueify the results by primary key.  Quick items don't have
    // unique primary keys, but when the same they refer to the same
    // item.

    while($v=$this->fetch()){
      $got[$v[$c::PRIMARY_KEY]]=$v;
      # Have some kind of max number of fetches here?
    }
    
    switch(count($got)){
    case 0:
      return null;
    case 1:
      //return array_values($got)[0];
      break;
    default: // >1
      if(method_exists($c,'find')){
	return $c::find($error_hint,array_values($got));
      }
      throw New \Exception
	(sprintf("Expecting 1 result many for '%s'",
		 $error_hint));
    }
    $this->row=array_values($got)[0];
    return array_values($got)[0];
  }

  # Group results by primary_key id (usually unique, but not in all
  # the quick database tables, the carps if we don't only have one.
  public function fetch_only_one($error_hint){
    $out=$this->fetch_one($error_hint);
    if(null==$out){
      throw New \Exception
	(sprintf("Expecting 1 result none for '%s'",$error_hint));

    }
    return $out;
  }

  
  public function message($row,$msg){
    $c=get_called_class();
    return sprintf('Where %s=%d %s',$c::PRIMARY_KEY,$row[$c::PRIMARY_KEY],
		   $msg);
  }

  public function insert(){
    $c=get_called_class();
    $dbh=$this->pdo();

    // Should figure a way to cache this result, but for now
    $sth=$dbh->prepare($c::INSERT_SQL);

    $ip=[]; # input_parameters
    foreach($this->qs as $k => $v){
      $ip[":$k"]=$v;
    }
    if(!$sth->execute($ip)){
      $dbh->rollBack();
      print "Error inserting inte $c::TABLE";
      exit(1);
      #return false;
    }
    return $dbh->lastInsertId();
  }

} // _Table

// this is a class that is used to get data about tables, that works
// like a _Table class, but it isn't an actual table in the database.
class Schema extends _Table{
  public function query(){
    $table=table_factory($this->cfg,['table'=>$this->qs['table_name']]);
    $this->fetched=$table->status_options();
  }
  public function fetch(){
    $out=$this->fetched;
    if($out){
      $this->fetched=false;
      return
	[
	 'table'=>$this->qs['table_name'],
	 'statuses'=>$out,
	 ];
    }
    return $out;
  }
}

class _Quick extends _Table{
  const DB='quick';
}

class Quick_organisms extends _Quick
{
  const TABLE='quick_organisms';
  const PRIMARY_KEY='organism_id';
  const ORDER_BY='organism_common_name';
}

class Quick_identifiers extends _Quick
{
  const TABLE='quick_identifiers';
  const PRIMARY_KEY='gene_id'; // not unique
  const SEARCH_COLUMN='quick_identifier_value';

  // static function
  public function find($needle,$haystack){
    // Not using needle, yet.
    foreach($haystack as $straw){
      if($straw['quick_identifier_type']=='OFFICIAL SYMBOL'){
	return $straw;
      }
    }

    throw New \Exception
      (sprintf("Can't pick '%s' from %d results.",
	       $needle,count($haystack)));
  }
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
  const INSERT_SQL='INSERT INTO interactions(publication_id,interaction_type_id,interaction_source_id)VALUES(:publication_id,:interaction_type_id,1)';
  
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

      $io=new Interaction_ontologies
	($this->cfg,['interaction_id'=>$v['interaction_id']]);
      $v['ontologies']=$io->count();

      # Now get interaction_notes
      $in=new Interaction_notes
	($this->cfg,['interaction_id'=>$v['interaction_id']]);
      $v['interaction_note_id']=$in->ids();

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
  // Need double ORDER_BY because some history items have the same timestamp.
  const ORDER_BY='interaction_history_date DESC, interaction_history_id DESC';
  const INSERT_SQL='INSERT INTO interaction_history(modification_type,interaction_id,user_id,interaction_history_comment)VALUES(:modification_type,:interaction_id,:user_id,:interaction_history_comment)';

  // Not really the status column, as it should not change, but it
  // sortta like a status column.
  const STATUS_COLUMN='modification_type';
}

class Interaction_ontologies extends _Table
{
  const TABLE='interaction_ontologies';
  const PRIMARY_KEY='interaction_ontology_id';
  const STATUS_COLUMN='interaction_ontology_status';
  const DEFAULT_STATUS='active';
  const INSERT_SQL='INSERT INTO interaction_ontologies(interaction_id,ontology_term_id,interaction_ontology_type_id,user_id)VALUES(:interaction_id,:ontology_term_id,:interaction_ontology_type_id,:user_id)';
}

class Interaction_ontology_types extends _Table
{
  const TABLE='interaction_ontology_types';
  const PRIMARY_KEY='interaction_ontology_type_id';
  const STATUS_COLUMN='interaction_ontology_type_status';
  const DEFAULT_STATUS='active';
}

class Interaction_sources extends _Table
{
  const TABLE='interaction_sources';
  const PRIMARY_KEY='interaction_source_id';
  const STATUS_COLUMN='interaction_source_status';
  const DEFAULT_STATUS='active';
}

class Interaction_notes extends _Table
{
  const TABLE='interaction_notes';
  const PRIMARY_KEY='interaction_note_id';
  const STATUS_COLUMN='interaction_note_status';
  const DEFUALT_STATUS='active';
  const INSERT_SQL='INSERT INTO interaction_notes(interaction_note_text,interaction_id,user_id)VALUES(:interaction_note_text,:interaction_id,:user_id)';
}

class Interaction_types extends _Table
{
  const TABLE='interaction_types';
  const PRIMARY_KEY='interaction_type_id';
  #const NAME_COLUMN='participant_type_name';
  const STATUS_COLUMN='interaction_type_status';
  const DEFAULT_STATUS='active';
}

class Interaction_participants extends _Table
{
  const TABLE='interaction_participants';
  const PRIMARY_KEY='interaction_participant_id';
  const STATUS_COLUMN='interaction_participant_status';
  const DEFAULT_STATUS='active';
  const INSERT_SQL='INSERT INTO interaction_participants(interaction_id,participant_id,participant_role_id)VALUES(:interaction_id,:participant_id,:participant_role_id)';
}

require_once('Ontologies.php');

class Ontology_terms extends _Table
{
  const TABLE='ontology_terms';
  const PRIMARY_KEY='ontology_term_id';
  const STATUS_COLUMN='ontology_status';
  const DEFALUT_STATUS='active';

  // Use only on small ontologies!
  public function tree(){
    $this->query();
    $ot=$this->fetch();

    $ors=new Ontology_relationships($this->cfg,['ontology_term_id'=>$ot['ontology_term_id']]);
    $ors->query();
    $or=$ors->fetch();

    //  If no relationships just return a list of items. 
    if(null==$or){
      $out=[];
      while($ot){
	array_push($out,$ot);
	$ot=$this->fetch();
      }
      return $out;
    }

    // else, if we have relationships
    $out=[];
    while($ot){
      $op_id=$or['ontology_parent_id'];
      if(null==$op_id){
	$out['root']=$ot;
      }else{
	if(array_key_exists($op_id,$out)){
	  array_push($out[$op_id],$ot);
	}else{
	  $out[$op_id]=[$ot];
	}
      }
      
      $ot=$this->fetch();
      if($ot){
	$ors=new Ontology_relationships($this->cfg,['ontology_term_id'=>$ot['ontology_term_id']]);
	$ors->query();
	$or=$ors->fetch_one('tree');
      }
    }
    return $out;
  }
}

class Ontology_relationships extends _Table
{
  const TABLE='ontology_relationships';
  const PRIMARY_KEY='ontology_relationship_id';
  const STATUS_COLUMN='ontology_relationship_status';
  const DEFAULT_STATUS='active';
}

class Unknown_participants extends _Table
{
  const TABLE='unknown_participants';
  const PRIMARY_KEY='unknown_participant_id';
  const STATUS_COLUMN='unknown_participant_status';
  const DEFAULT_STATUS='active';
}

class Participant_roles extends _Table
{
  const TABLE='participant_roles';
  const PRIMARY_KEY='participant_role_id';
  const STATUS_COLUMN='participant_role_status';
  const DEFAULT_STATUS='active';
}

class Participant_types extends _Table
{
  const TABLE='participant_types';
  const PRIMARY_KEY='participant_type_id';
  const STATUS_COLUMN='participant_type_status';
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
      //trigger_error($this->message($out,"fetched MEDLINE for PMID:".$out[self::SEARCH_COLUMN]),E_USER_NOTICE);
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

class Project_publications extends _Table
{
  const TABLE='project_publications';
  const PRIMARY_KEY='project_publication_id';
  const ORDER_BY='publication_pubmed_id';

  // Grab publication_pubmed_id so save an ajax call.
  public function _select(){
    $c=get_called_class();
    return 'SELECT project_publication_id,project_id,publication_id,' .
      'project_publication_addeddate,project_publication_status,'     .
      'publication_query_id,publication_pubmed_id FROM '              .
      $c::TABLE . ' JOIN publications USING(publication_id)';
  }
}

class Project_users extends _Table
{
  const TABLE='project_users';
  const PRIMARY_KEY='project_user_id';
}

class Projects extends _Table
{
  const TABLE='projects';
  const PRIMARY_KEY='project_id';
}

/* Used for in ../user.php for auth. */
class User extends _Table
{
  const TABLE='users';
  const PRIMARY_KEY='user_id';
}

/* Doesn't return password related stuff. */
class Users extends _Table
{
  const TABLE='users';
  const PRIMARY_KEY='user_id';

  protected function columns(){
    return 'user_id,user_name,user_firstname,user_lastname,user_status';
  }
}

// wee but of a buffer so you can't query any table you would like.
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
  case 'interaction_ontologies':
    return new Interaction_ontologies($cfg,$qs);
  case 'interaction_ontology_types':
    return new Interaction_ontology_types($cfg,$qs);
  case 'interaction_participants':
    return new Interaction_participants($cfg,$qs);
  case 'interaction_sources':
    return new Interaction_sources($cfg,$qs);
  case 'interaction_notes':
    return new Interaction_notes($cfg,$qs);
  case 'interaction_types':
    return new Interaction_types($cfg,$qs);
  case 'ontology_terms':
    return new Ontology_terms($cfg,$qs);
  case 'participants':
    return new Participants($cfg,$qs);
  case 'participant_roles':
    return new Participant_roles($cfg,$qs);
  case 'participant_types':
    return new Participant_types($cfg,$qs);
  case 'publications':
    return new Publications($cfg,$qs);
  case 'project_publications':
    return new Project_publications($cfg,$qs);
  case 'project_users':
    return new Project_users($cfg,$qs);
  case 'projects':
    return new Projects($cfg,$qs);
  case 'quick_identifiers':
    return new Quick_identifiers($cfg,$qs);
  case 'quick_identifier_types':
    return new Quick_identifier_types($cfg,$qs);
  case 'quick_organisms':
    return new Quick_organisms($cfg,$qs);
  case 'schema':
    return new Schema($cfg,$qs);
  case 'unknown_participants':
    return new Unknown_participants($cfg,$qs);
  case 'users':
    return new Users($cfg,$qs);
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
