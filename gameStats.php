<?php

  $dir = getcwd().'/gamestats/';
  if (file_exists($dir.$_GET["gameID"]))
  {
    $out = readfile($dir.$_GET["gameID"]);
  }

?>
