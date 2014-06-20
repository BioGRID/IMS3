<!DOCTYPE html>
<?php
require_once('ims/ims.php');
$ims=new IMS\config('ims.json');
?>
<html lang="en"><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">
<title>IMS3</title>
<?php print $ims->html_head(); ?>
</head><body>

<div class="container">

  <h1>IMS3</h1>

  <header>
  <input type="hidden" id="pubmed" style="width:90%">
  </header>



  <div class="row">

  <div class="col-md-9">
  <h1>Interactions <span class="interaction_count"></span></h1>
  <table class="table"><tbody id="interactions"></tbody></table>
  </div>

  <aside class="col-md-3">

  <h1>Messages <span class="message-count"></span></h1>
  <div id="messages"><p>Nothing</p></div>

  <h1>Publication</h1>
  <div class="panel-group" id="publication"><div class="panel panel-default"></div></div>

  </aside>

</div>


</body></html>
