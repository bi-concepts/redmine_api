<?php
/** 
  * PHP Skript für Python API-Aufruf
  *
  * @author BI-Concepts GmbH
  * @param t -> task as string (getissueinfo -gii)
  * @param i -> id as integer
  * @param v -> value as integer
  * @return
  */
  
// POST & GET Variablen deklarieren
$HTTP_POST_VARS    = !empty($HTTP_POST_VARS)    ? $HTTP_POST_VARS    : $_POST;
$HTTP_GET_VARS     = !empty($HTTP_GET_VARS)     ? $HTTP_GET_VARS     : $_GET;
$HTTP_COOKIE_VARS  = !empty($HTTP_COOKIE_VARS)  ? $HTTP_COOKIE_VARS  : $_COOKIE;
$HTTP_SERVER_VARS  = !empty($HTTP_SERVER_VARS)  ? $HTTP_SERVER_VARS  : $_SERVER;

//GET VARS
if (isset($HTTP_GET_VARS["t"])){$task=$HTTP_GET_VARS["t"];}else{$task='';}
if (isset($HTTP_GET_VARS["i"])){$id=$HTTP_GET_VARS["i"];}else{$id='';}
if (isset($HTTP_GET_VARS["v"])){$value=$HTTP_GET_VARS["v"];}else{$value='';}


//Funktion einbinden
include_once('functions.php');

//Werte pruefen
$werteok=0;
$task_value=array("gii","uis","uip","sin");
if(in_array($task,$task_value)){
 if(is_numeric($id)){ 
  if(is_numeric($value)){
  	$werteok=1;
  }
 }
}
 
//Python Skript via exec ausfuehren
if($werteok===1){  
  exec("python3 /var/www/html/redmine/redmine_api/rm_rest_api.py $task $id $value", $ausgabe);
}else{die('Error');}
echo json_encode($ausgabe);


//Ausgabe als XML
//$xml_data = new SimpleXMLElement("<data></data>");
//echo $xml_data->asXML();
echo array2XML($ausgabe);

?>
