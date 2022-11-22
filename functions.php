<?php
/** 
  * PHP Funktionssammlung
  *
  * @author BI-Concepts GmbH
  * @param
  * @return
  */
  
//Funktion array2XML
function array2xml($array, $rootElement = null, $xml = null){
 $_xml=$xml;
 if ($_xml === null){ $_xml = new SimpleXMLElement($rootElement !== null ? $rootElement : '<root/>');}
 
 foreach ($array as $key => $value){
    //untere Felder aufloesen
  if (is_array($value)){
     array2XML($value, $key, $_xml->addChild($key));
  }else{
  	$_xml->addChild($key,$value);
  }
 }
 return $_xml->asXML();
}

?>
