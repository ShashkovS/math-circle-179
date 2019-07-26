<?php


define('IN_CONDUIT', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(PUPIL_LEVEL);
require_once('FillSelectors.inc');

// Получаем класс и листок для кондуита
if (isset($_COOKIE['Class'])) {
    $ClassID = (string)mysql_real_escape_string($_COOKIE['Class']);
} else {
    unset($ClassID);
}

if (isset($_COOKIE['List'])) {
    $ListID = (string)mysql_real_escape_string($_COOKIE['List']);
} else {
    unset($ListID);
}

?>
<!DOCTYPE HTML>
<!-- 
Лучше всего сайт работает в FireFox (4+). 
В Chrome и Opera тоже в целом работает. 
В IE очевидным образом не работает совсем. 
В Safari не тестировался.
-->
<html>
<head>

    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    
    <title>Менеджер кондуитов</title>

    <!-- Подключаем jQuery и jQuery UI (DatePicker) -->
    <script type="text/javascript" src="http://yandex.st/jquery/1.7.0/jquery.min.js"></script>
    <script type="text/javascript" src="js/jquery-ui-1.8.13.custom.min.js"></script>
    <script type="text/javascript" src="js/ui.datepicker-ru.min.js"></script>
    <link type="text/css" href="css/jquery.ui/datepicker.css" rel="stylesheet" />
    <link type="text/css" href="css/jquery.ui/theme.css" rel="stylesheet" />
    <link type="text/css" href="css/jquery.ui/core.css" rel="stylesheet" />
    <!-- Подключаем jQuery Cookie plugin -->
    <script type="text/javascript" src="http://yandex.st/jquery/cookie/1.0/jquery.cookie.min.js"></script>
    <!-- Подключаем эмулятор LocalStorage -->
    <script type="text/javascript" src="js/localStorage.min.js"></script>
    <!-- Подключаем jQuery FloatHeader plugin -->
    <script type="text/javascript" src="js/jquery.floatheader-1.4.js"></script>
    <!-- Подключаем движок кондуита -->
    <script type="text/javascript" src="js/Conduit.js"></script>
    <link rel="stylesheet" href="css/Conduit.css">
    <script type="text/javascript" src="js/MathML.js"></script>
    <link rel="stylesheet" href="css/MathML.css">
    <!-- Подключаем панели инструментов -->
    <script type="text/javascript" src="js/Bars.js"></script>
    <link type="text/css" href="css/Bars.css" rel="stylesheet" />

    <script type="text/javascript">
        NavBar = new __NavBar('Conduit');
        ToolBar = new __ToolBar();    
    </script>
</head>

<body onload="Conduit.init()" onkeyup="Conduit.onkey(event)">

    <header>
<?php require('Navbar.inc'); ?>
<?php require('ConduitToolbar.inc'); ?>
    </header>
    
    <section id="conduit_container">
        <p id="loading">
            Ждите. Производится получение данных с сервера...
        </p>
    </section>
<!-- Yandex.Metrika counter --><div style="display:none;"><script type="text/javascript">(function(w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter10427686 = new Ya.Metrika({id:10427686, enableAll: true, ut:"noindex"}); } catch(e) { } }); })(window, "yandex_metrika_callbacks");</script></div><script src="//mc.yandex.ru/metrika/watch.js" type="text/javascript" defer="defer"></script><noscript><div><img src="//mc.yandex.ru/watch/10427686?ut=noindex" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->
</body>
</html>