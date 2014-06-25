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

  <h1 id="title"><?php print $ims->title(); ?> <span class="version">Ver:<?php print $ims->version(); ?></span></h1>

  <header>
  <input type="hidden" id="pubmed" style="width:90%">
  </header>



  <div class="row">

  <div class="col-md-9">
  <h1>Interactions <span class="interaction_count"></span></h1>
  <table class="table"><tbody id="interactions"></tbody></table>
  </div>

  <aside class="col-md-3">

  <h1>Messages (<span class="message-count">0</span>)</h1>
  <div id="messages"></div>

  <h1>Publication</h1>
  <div class="panel-group" id="publication"><div class="panel panel-default"></div></div>

  </aside>

</div>


</body></html>
