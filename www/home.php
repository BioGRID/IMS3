<!DOCTYPE html>
<?php
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
<script src="Publication.js"></script>
<script src="Interaction.js"></script>
<script src="Interaction_source.js"></script>
<script src="Interaction_type.js"></script>
</head><body>


<div class="container">
  <div class="starter-template">
  <h1 id="title"><?php print $ims->title(); ?> <small>Ver:<?php print $ims->version(); ?></small></h1>
  </div>
</div>

<div class="container">
  <div class="row">
  <div class="col-md-9">


  <!-- h1>Something Else</h1>
  <p>Some text here.</p -->


  <h1>Interactions <span class="interaction_count"></span></h1>
  <input type="hidden" id="pubmed" style="width:100%">
  <table class="table table-hover"><tbody id="interactions"></tbody></table>

  </div><!-- .col-md-9 -->

  <aside class="col-md-3">

  <h1>Messages (<span class="message-count">0</span>)</h1>
  <div id="messages"></div>

  <h1>Publication</h1>
  <div class="panel-group" id="publication"><div class="panel panel-default"></div></div>

  </aside><!-- .col-md-3 -->

</div>


</body></html>
