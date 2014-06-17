<?php
require_once('../php/ims.php');
IMS\divert_errors();
$cfg=new IMS\config('../ims.json');
$table=IMS\table_factory($cfg,$_GET);
if($table){
  $table->query();
  IMS\pdo2json($table);
}else{
  IMS\messages2json();
}
