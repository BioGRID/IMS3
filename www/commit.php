<?php

  /*
    Takes POST input like:
    { publicaton_id =>
     [
      [ interaction_type_id,{
        'participants':[
         {'role_id':role_id,'participant_type_id':participant_type_id,...}...
        ],
      }
     ],
      publication_id => ...
    }

    Depending on participant_type_id there might be other options.
    When participant_type_id==1 (gene), currently only supported:
       'organism_id','quick_participant_value'

    
   */

require_once('ims/ims.php');
$cfg=new IMS\config('ims.json');
$user=$cfg->verify_user_or_die();
$user_id=$user['user_id'];

$dbh=(new IMS\_Table($cfg,[]))->pdo();
$dbh->beginTransaction();

//var_dump($_POST);
//exit(1);

foreach($_POST as $publication_id => $interactions){

  # For now we will assume the passed publication_id is accurate.
  foreach($interactions as $interaction){
    $interaction_type_id=array_shift($interaction);
    $interaction=$interaction[0];

    $i=new IMS\Interactions
      ($cfg,
       ['publication_id'=>$publication_id,
	'interaction_type_id'=>$interaction_type_id]);
    $interaction_id=$i->insert();

    # lets log it
    $ih=new IMS\Interaction_history
      ($cfg,
       ['modification_type'=>'ACTIVATED',
	'interaction_id'=>$interaction_id,
	'user_id'=>$user_id,
	'interaction_history_comment'=>'IMS3 Created',
	]);
    $ih->insert();

    // Insert any notes we might have
    if(array_key_exists('notes',$interaction)){
      foreach($interaction['notes'] as $note){
	$in=new IMS\Interaction_notes
	  ($cfg,
	   ['interaction_note_text'=>$note,
	    'interaction_id'=>$interaction_id,
	    'user_id'=>$user_id,
	    ]);
	$in->insert();
      }
    }

    foreach($interaction['ontologies'] as $ontology){
      $args=['interaction_id'=>$interaction_id,
	     'user_id'=>$ontology['user_id'],
	     'ontology_term_id'=>$ontology['term_id']];

      // As type_id in optional we make sure it exists before using it
      if(array_key_exists('type_id',$ontology)){
	$args['interaction_ontology_type_id']=$ontology['type_id'];
      }else{
	$args['interaction_ontology_type_id']=null;
      }
      $io=new IMS\Interaction_ontologies($cfg,$args);
      $interaction_ontology_id=$io->insert();

      // Again, as qualifier_id is option we don't want to try to
      // insert anything unless we have something to insert.
      if(array_key_exists('qualifier_ids',$ontology)){
	foreach($ontology['qualifier_ids'] as $qualifier_id){
	  $ioq=new IMS\Interaction_ontologies_qualifiers
	    ($cfg,
	     ['interaction_ontology_id'=>$interaction_ontology_id,
	      'ontology_term_id'=>$qualifier_id,
	      'user_id'=>$user_id
	      ]);
	  $ioq->insert();
	}
      }
    }

    foreach($interaction['participants'] as $participant){
      $participant_role_id=$participant['role_id'];
      $participant_type_id=$participant['participant_type_id'];

      if(1!=$participant_type_id){
	print "I only do genes.";
	exit(0);
      }

      // Spicific to genes
      $quick_identifier_value=$participant['quick_participant_value'];
      $organism_id=$participant['organism_id'];

      // Get the gene_id
      $qi=new IMS\Quick_identifiers
	($cfg,
	 ['organism_id'=>$organism_id,
	  'quick_identifier_value'=>$quick_identifier_value]);
      $qi->query();
      $gene=$qi->fetch_only_one($quick_identifier_value);
      $gene_id=$gene['gene_id'];
      
      // get the participant_id
      $p=new IMS\Participants
	($cfg,
	 ['participant_value'=>$gene_id,
	  'participant_type_id'=>$participant_type_id,
	  ]);
      $p->query();
      $participant=$p->fetch_only_one($quick_identifier_value);
      $participant_id=$participant['participant_id'];
      // If we don't get a participant we should create one here.

      // Insert into the interaction_participants table 
      $ip=new IMS\Interaction_participants
	($cfg,
	 ['interaction_id'=>$interaction_id,
	  'participant_id'=>$participant_id,
	  'participant_role_id'=>$participant_role_id,
	  ]);
      $ip->insert();
    }
  }
}

print json_encode('OK');
$dbh->commit();