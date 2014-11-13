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
<script src="Interaction_participant.js"></script>
<script src="Interaction_source.js"></script>
<script src="Interaction_type.js"></script>
<script src="Participant.js"></script>
<script src="Participant_role.js"></script>
<script src="Participant_type.js"></script>
<script src="Publication.js"></script>
<script src="Quick_identifier.js"></script>
<script src="Quick_identifier_type.js"></script>
<script src="Quick_organism.js"></script>
<script src="Unknown_participant.js"></script>
<?php # <script src="convert.js"></script> ?>
</head><body>

<div class="container-fluid">
<h1 id="title"><?php print $ims->title(); ?> <small>Ver:<?php print $ims->version(); ?></small></h1>
<p class="h6" id="user"></p>
</div>

<div class="container-fluid">
<ul class="nav nav-tabs">
  <?php # <li><a href="#log_tab" data-toggle="tab">Log (<span class="log-count">0</span>)</a></li> ?>
  <li class="active"><a href="#interaction_tab" data-toggle="tab">Interactions</a></li>
  <?php # <li><a href="#conversion" data-toggle="tab">ID Conversion</a></li> ?>
</ul>
</div>

<div class="tab-content container-fluid">
  <?php # include("ims/html/log.htm") ?>

  <div class="tab-pane active" id="interaction_tab">
    <h1>Publication</h1>
    <input type="hidden" id="pubmed" style="width:100%">
    <blockquote class="dropdown" id="publication"></blockquote>

    <div class="ifpub hidden">
      <h1>Create Interaction
	<select class="interaction_types h5"></select>
      </h1>

      <div class="container-fluid hidden user">
	<div class="row">
	  <fieldset class="col-md-4 interactions colA">
	    <legend>Column A</legend>
	    <input type="hidden" name="role">
	    <select class="quick_organism"></select>
	    <textarea></textarea>
	  </fieldset>
	  <fieldset class="col-md-4 interactions colB" disabled>
	    <legend>Column B</legend>
	    <input type="hidden" name="role">
	    <select class="quick_organism"></select>
	    <textarea></textarea>
	  </fieldset>
	  <div class="col-md-4">
	    <p>Fav ontology terms go here.</p>
	  </div>
	</div><!-- .row -->
	<p><button id="commit">Commit</button></p>
      </div>
      
      <h2>Interactions</h2>
      <div class="pager">
	Page: <select class="gotoPage"></select>
	<button class="first" title="First page">⇤</button>
	<button class="prev" title="Previous page">←</button>
	<span class="pagedisplay"></span>
	<button class="next" title="Next page">→</button>
	<button class="last" title="Last page">⇥</button>
	<select class="pagesize">
	  <option value="5">5</option>
	  <option selected="selected" value="10">10</option>
	  <option value="20">20</option>
	  <option value="30">30</option>
	  <option value="40">40</option>
	</select>
      </div> 
      <table class="interactions table table-hover"><thead/><tbody/></table>

      <h2>Participants</h2>
      <div class="pager">
	Page: <select class="gotoPage"></select>
	<button class="first" title="First page">⇤</button>
	<button class="prev" title="Previous page">←</button>
	<span class="pagedisplay"></span>
	<button class="next" title="Next page">→</button>
	<button class="last" title="Last page">⇥</button>
	<select class="pagesize">
	  <option value="5">5</option>
	  <option selected="selected" value="10">10</option>
	  <option value="20">20</option>
	  <option value="30">30</option>
	  <option value="40">40</option>
	</select>
      </div> 

      <table class="participants table table-hover"><caption>
	  <dl class="footnotes dl-horizontal">
	    <dt class="asterisk hide">*</dt><dd class="asterisk hide">Unknown Participant</dd>
	  </dl>
	</caption><thead/><tbody/></table>
    </div><!-- ifpub -->

  </div>

  <?php # include('ims/html/convert.htm'); ?>

</div><?php # tab-content ?>

</body></html>
