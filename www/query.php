<?php
require_once('ims/ims.php');
IMS\divert_errors();
$cfg=new IMS\config('ims.json');
$table=IMS\table_factory($cfg,$_GET);
$table->query();
IMS\pdo2json($table);
