<?php

if (!defined('IN_CONDUIT')){
    // Попытка прямого доступа к файлу
    exit();
}
require_once('Connect.inc');

// Возможные группы пользователей
define('_ADMIN',    'Admin');
define('_TEACHER',  'Teacher');
define('_PUPIL',    'Pupil');
define('_DISABLED', 'Disabled');

define('ADMIN_LEVEL',  100);
define('TEACHER_LEVEL', 20);
define('PUPIL_LEVEL',   10);
define('DISABLED_LEVEL', 0);

$UserLevel[_DISABLED]    = DISABLED_LEVEL;
$UserLevel[_PUPIL]       = PUPIL_LEVEL;
$UserLevel[_TEACHER]     = TEACHER_LEVEL;
$UserLevel[_ADMIN]       = ADMIN_LEVEL;

// Имя пользователя
$USERNAME = $_SERVER['REMOTE_USER'];

// Определяем уровень доступа пользователя
$sql = 'SELECT `Group`, `DisplayName` FROM `PUser` WHERE `User` = "' . $USERNAME . '" AND `Disabled` = "N"';
$result = mysql_query($sql);
if(!$result) {
    trigger_error('Selection error: ' . mysql_error());
}
if ($row = mysql_fetch_array($result)) {
    $GROUP = $row['Group'];
    $USERDISPLAYNAME = $row['DisplayName'];
} else {
    $GROUP = _DISABLED;
}

$USERLEVEL = $UserLevel[$GROUP];

// Сравниваем уровни доступа пользователя и запрашиваемой страницы
function checkAccess($PageLevel) {
    global $USERLEVEL;
    if ($USERLEVEL < $PageLevel) {
        if (!defined('AJAX')) {
            //require_once('NoAccess.php');
            require_once('404.html');
        }
        exit();
    }
}

?>