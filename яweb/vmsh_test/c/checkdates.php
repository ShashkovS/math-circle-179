<?php
$file = $_GET["file"];
if ($file == "") {
  exit();
}

$ext = substr(strrchr($file, "."), 1);

switch ($ext) {
  case "png" : $num = substr($file,0,4); break;
  case "pdf" : $num = substr($file,0,4); break;
  case "html" : $num = substr($file,0,4); $ext = $ext.".".substr($file,4,3); break;
  default: exit();
}


require_once('../dates.inc');

$lesdt = $datesarr[$num];
if (!$lesdt) {
  exit();
}

$curdt = new DateTime;
$weekdt = new DateTime;
$monthdt = new DateTime;
    # админу можно всё ;-)
    if (isset($_COOKIE['admin']) && md5('admin57') === $_COOKIE['admin']) {
      $curdt->modify('+1000 day');
      $weekdt->modify('+1000 day');
      $monthdt->modify('+1000 day');
    } elseif (isset($_COOKIE['cond']) && md5('cond') === $_COOKIE['cond']) {
      $weekdt->modify('-7 day');
      $monthdt->modify('-28 day');
    } else {
      $weekdt = new DateTime("2015-09-29T19:00:00Z");
      $monthdt->modify('-1000 day');
    }

switch ($ext) {
  case "png" : 
    if ($lesdt->format('Y-m-d H:i:s') > $curdt->format('Y-m-d H:i:s')) {
      exit();
    }
    // if (!isset($_SERVER['HTTP_REFERER']) or ($_SERVER['HTTP_REFERER'] != "http://www.shashkovs.ru/vmsh_2016/" and $_SERVER['HTTP_REFERER'] != "https://www.shashkovs.ru/vmsh_2016/")) {
    //   exit();
    // }
    if (isset($_SERVER['HTTP_IF_MODIFIED_SINCE'])) {
      header('HTTP/1.1 304 Not Modified'); exit();
    }
    $path = "../i/$file";
    header('Last-Modified: Wed, 11 Nov 2015 07:45:54 GMT');
    // $LastModified_unix=filemtime($path);
    // $LastModified = gmdate("D, d M Y H:i:s \G\M\T", $LastModified_unix);    
    // header('Last-Modified: '. $LastModified);
    header('Content-type: image/png');
    header('Cache-Control: max-age=604800, public');
    break;
  case "pdf" :
    if ($lesdt->format('Y-m-d H:i:s') > $curdt->format('Y-m-d H:i:s')) {
      exit();
    }
    $path = "../data/$file";
    header('Content-type: application/pdf');
    header('Content-Disposition: inline; filename="' . $file . '"');
    break;
  case "html.les" : 
    if ($lesdt->format('Y-m-d H:i:s') > $curdt->format('Y-m-d H:i:s')) {
      exit();
    }
    $path = "../data/$file";
    header('Content-type: text/html');
    break;
  case "html.sol" : 
    if ($lesdt->format('Y-m-d H:i:s') < $monthdt->format('Y-m-d H:i:s')) {
      header('Content-type: text/html');
      $path = "../data/".$num."-solution.html";
    } elseif ($lesdt->format('Y-m-d H:i:s') < $weekdt->format('Y-m-d H:i:s')) {
      header('Content-type: text/html');
      $path = "../data/".$num."-solution0.html";
    } else {
      exit();
    }
    break;
  default: exit();
}
if (file_exists($path)) {
  ob_clean();
  flush();
  readfile($path);
}
exit();
?>
