<?php

if (!defined('IN_CONDUIT')){
    // Попытка прямого доступа к файлу
    exit();
}
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/PrivateData/conduit/config.php');

// Коннект к базе
$conn = mysql_connect($dbhost, $dbuser, $dbpasswd);
if (!$conn) {
    trigger_error('Could not connect to database: ' . mysql_error());
}
// Теперь логин и пароль можно забыть навсегда
unset($dbuser);
unset($dbpasswd);

// Выбираем схему
mysql_select_db($dbname);

// При необходимости явно указываем кодировку соединения
mysql_set_charset('utf8');
date_default_timezone_set('Europe/Moscow');


?>