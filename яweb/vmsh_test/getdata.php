<?php
    define('IN_VMSH', true);
    define('AJAX', true);
    require_once('dates.inc');

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
    
    $type = (string)($_POST['Type']);
    $number = (string)($_POST['Number']);

    if (strlen($number) > 5 or !($type === 'solution')) {
      echo "Решения задач появляются не раньше, чем через неделю после ВМШ."; exit();
    }
    $lesdt = $datesarr[$number];
    if (!$lesdt) {
      echo "Решения задач появляются не раньше, чем через неделю после ВМШ."; exit();
    }
    if ($lesdt->format('Y-m-d H:i:s') < $monthdt->format('Y-m-d H:i:s')) {
      if(file_exists("data/{$number}-solution.html")) {
    include("data/{$number}-solution.html");
    } else {
      echo "Решения задач появляются не раньше, чем через неделю после ВМШ. Решения будут скоро готовы."; exit();
    }
    } elseif ($lesdt->format('Y-m-d H:i:s') < $weekdt->format('Y-m-d H:i:s')) {
      if(file_exists("data/{$number}-solution0.html")) {
    include("data/{$number}-solution0.html");
    } else {
      echo "Решения задач появляются не раньше, чем через неделю после ВМШ. Решения будут скоро готовы."; exit();
    }
    } else {
      echo "Решения задач появляются не раньше, чем через неделю после ВМШ."; exit();
    }
?>