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
<script src="Interaction_participant.js"></script>
<script src="Interaction_source.js"></script>
<script src="Interaction_type.js"></script>
<script src="Participant.js"></script>
<script src="Participant_role.js"></script>
<script src="Publication.js"></script>
<script src="Quick_identifiers.js"></script>
</head><body>

<h1 id="title"><?php print $ims->title(); ?> <small>Ver:<?php print $ims->version(); ?></small></h1>

<div class="container">
<ul class="nav nav-tabs">
  <li><a href="#log_tab" data-toggle="tab">Log (<span class="log-count">0</span>)</a></li>
  <li class="active"><a href="#interaction_tab" data-toggle="tab">Interactions</a></li>
  <!-- li><a href="#conversion" data-toggle="tab">ID Conversion</a></li -->
</ul>
</div>

<div class="tab-content container">

  <div class="tab-pane" id="log_tab">
    <h1>Messages</h1>
    <button class="btn btn-primary" onclick="$('#log').html('');$('.log-count').html(0)">Clear Log</button>
    <button class="btn btn-primary" data-toggle="modal" data-target="#localStorage" onclick="IMS.localStorage_dl()">View localStorage</button>

    <div id="log"></div>

    <div class="modal fade" id="localStorage">
      <div class="modal-dialog">
	<div class="modal-content">
	  <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
            <h4 class="modal-title">Modal title</h4>
	    <p>Here is the data being stored using
	    the <a target="_blank"
	    href="http://www.w3.org/TR/webstorage/#dom-localstorage">localStorage</a>
	    feature.  If it look
	    currupt <a href="https://github.com/svenmh/IMS3/issues">report
	    it</a> and clear it.</p>
	  </div>
	  <div class="modal-body">
	  </div>
	  <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" onclick="localStorage.clear();IMS.localStorage_dl()">Clear localStorage</button>
	  </div>
	</div><!-- .modal-content -->
      </div><!-- .modal-dialog -->
    </div><!-- .modal -->

  </div><!-- #log_tab -->

  <div class="tab-pane active" id="interaction_tab">
    <h1>Publication</h1>
    <input type="hidden" id="pubmed" style="width:100%">
    <blockquote class="dropdown" id="publication"></blockquote>
    <h2>Interactions <span class="interaction-count"></span></h2>
    <table id="interactions" class="table table-hover"><thead/><tbody/></table>
    <h3>Participants <span class="participant-count"></span></h3>
    <table id="participants" class="table"><thead/><tbody/></table>
  </div>

  <!-- div class="tab-pane" id="conversion">
    Yo!
  </div -->

</div>





</body></html>
