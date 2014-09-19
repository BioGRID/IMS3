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
<script src="Publication.js"></script>
<script src="Quick_identifier.js"></script>
<script src="Quick_identifier_type.js"></script>
<script src="Quick_organism.js"></script>
<script src="Unknown_participant.js"></script>
</head><body>

<div class="container">
<h1 id="title"><?php print $ims->title(); ?> <small>Ver:<?php print $ims->version(); ?></small></h1>
<p class="h6" id="user"></p>
</div>

<div class="container">
<ul class="nav nav-tabs">
  <li><a href="#log_tab" data-toggle="tab">Log (<span class="log-count">0</span>)</a></li>
  <li class="active"><a href="#interaction_tab" data-toggle="tab">Interactions</a></li>
  <li><a href="#conversion" data-toggle="tab">ID Conversion</a></li>
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
    </div><!-- .modal #localStorage -->

  </div><!-- #log_tab -->

  <div class="tab-pane active" id="interaction_tab">
    <h1>Publication</h1>
    <input type="hidden" id="pubmed" style="width:100%">
    <blockquote class="dropdown" id="publication"></blockquote>

    <div class="ifpub hidden">
      <h2>
	Interactions
	<span class="hidden user">
	  <select id="interaction_types"></select>
	  <button id="add_interaction">&#x2386;</button>
	</span>
      </h2>


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
      <table id="interactions" class="table table-hover"><thead/><tbody/></table>
      <h3>
	Participants
	<span class="hidden user">
	  <select id="participant_role"></select>
	  <button id="add_participant">&#x2386;</button>
	</span>
      </h3>
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

      <table id="participants" class="table"><caption>
	  <dl class="footnotes dl-horizontal">
	    <dt class="asterisk hide">*</dt><dd class="asterisk hide">Unknown Participant</dd>
	  </dl>
	</caption><thead/><tbody/></table>
    </div><!-- ifpub -->

  </div>

  <div class="tab-pane" id="conversion">
    <h1>ID Conversion</h1>
    <p>This is still very hackey, but hopefully it will improve as
    time goes by.  Plus, the BioGRID Quick database doesn't have every
    ID anyway.  The order of the output isn't the same as the order if
    the input. -Sven</p>

    <div clas="row">
      <div class="col-md-5" id="id-from">
	<select></select>
	<textarea></textarea>
	<dl class="dl-horizontal"></dl>
      </div><div class="col-md-2">
	<button id="conv" class="h1">&#10144;</button>
      </div><div class="col-md-5" id="id-to">
	<select></select>
	<textarea readonly></textarea>
	<dl class="dl-horizontal"></dl>
      </div>
    </div>

  </div>
</div>

<div class="modal fade" id="participant_selector">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
	<h1>Participant Selector</h1>
      </div><div class="modal-body">

	<ul class="nav nav-tabs">
	  <li class="active"><a href="#quick_participants" data-toggle="tab">Quick Participants</a></li>
	  <li><a href="#force_participants" data-toggle="tab">Forced Participants</a></li>
	</ul>

	<div class="tab-content container">
	  <div class="tab-pane active" id="quick_participants">
	    <p>Quick</p>
	  </div>
	  <div class="tab-pane" id="force_participants">
	    <p>Use the force Luke.</p>
	  </div>
	</div>

      </div><div class="modal-footer">
	<p>footer</p>
      </div>
    </div>
  </div>
<div>


</body></html>
