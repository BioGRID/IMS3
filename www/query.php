<?php
require_once('ims/ims.php');
IMS\divert_errors();
header('Content-type: text/plain');
$cfg=new IMS\config('ims.json');
$table=IMS\table_factory($cfg,$_GET);
$table->query();
IMS\pdo2json($table);
