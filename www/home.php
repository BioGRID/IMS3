<!DOCTYPE html><?php /* -*- mode: html -*- */
require_once('ims/ims.php');
$ims=new IMS\config('ims.json');
?>

<html lang="en"><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">
<title><?php print $ims->title(); ?></title>
<?php print $ims->html_head(); ?>
<link href="ims.css" rel="stylesheet"/>
<script src="ims.js"></script>
<script src="Interaction.js"></script>
<script src="Interaction_history.js"></script>
<script src="Interaction_ontology.js"></script>
<script src="Ontology.js"></script>
<script src="Ontology_term.js"></script> 
<script src="Interaction_ontology_qualifier.js"></script><? # inherits Ontoolgy_term ?>
<script src="Interaction_ontology_type.js"></script>
<script src="Interaction_participant.js"></script>
<script src="Interaction_source.js"></script>
<script src="Interaction_note.js"></script>
<script src="Interaction_type.js"></script>
<script src="Participant.js"></script>
<script src="Participant_role.js"></script>
<script src="Participant_type.js"></script>
<script src="Project.js"></script>
<script src="Publication.js"></script>
<script src="Quick_identifier.js"></script>
<script src="Quick_identifier_type.js"></script>
<script src="Quick_organism.js"></script>
<script src="Unknown_participant.js"></script>
<script src="User.js"></script>
<?php # <script src="convert.js"></script> ?>
</head><body>

<div class="container-fluid">
<h1 id="title"><?php print $ims->title(); ?> <small>Ver:<?php print $ims->version(); ?></small></h1>
<p class="h6" id="user"></p>
</div>

<div class="container-fluid">
<ul class="nav nav-tabs">
  <?php # <li><a href="#log_tab" data-toggle="tab">Log (<span class="log-count">0</span>)</a></li> ?>
  <li class="active"><a href="#project_tab" data-toggle="tab">Project</a></li>
  <li><a href="#interaction_tab" data-toggle="tab">Interactions</a></li>
  <?php # <li><a href="#conversion" data-toggle="tab">ID Conversion</a></li> ?>
</ul>
</div>

<div class="tab-content container-fluid">
  <?php
     #include('ims/html/log.htm');
     include('ims/html/project.htm');
     include('ims/html/interaction.htm');
     #include('ims/html/convert.htm');
     ?>

</div><?php # tab-content ?>

</body></html>
