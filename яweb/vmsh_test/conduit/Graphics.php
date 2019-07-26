<?php

define('IN_CONDUIT', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(PUPIL_LEVEL);
require_once('FillSelectors.inc');

// Получаем класс для отображения
if (isset($_COOKIE['Class'])) {
    $ClassID = (string)mysql_real_escape_string($_COOKIE['Class']);
} else {
    unset($ClassID);
}

?>
<!DOCTYPE HTML>

<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    
    <title>Графики</title>
    
    <!-- Подключаем jQuery -->
    <script type="text/javascript" src="js/jquery-1.6.1.min.js"></script>
    
    <!-- Подключаем jQuery Flot plugin -->
    <script type="text/javascript" src="js/jquery.flot.min.js"></script>
    <script type="text/javascript" src="js/jquery.flot.stack.min.js"></script>
    <script type="text/javascript" src="js/jquery.flot.selection.min.js"></script>
    <script type="text/javascript" src="js/jquery.flot.crosshair.min.js"></script>
 
    <!-- Подключаем jQuery Cookie plugin -->
    <script type="text/javascript" src="js/jquery.cookie.min.js"></script>

    <!-- Подключаем MathML -->
    <script type="text/javascript" src="js/MathML.js"></script>
    <link type="text/css" href="css/MathML.css" rel="stylesheet" />
    
    <!-- Подключаем саму рисовалку -->
    <script type="text/javascript" src="js/Graphics.js"></script>
    <link type="text/css" href="css/Graphics.css" rel="stylesheet" />
    
    <!-- Подключаем панели инструментов -->
    <script type="text/javascript" src="js/Bars.js"></script>
    <link type="text/css" href="css/Bars.css" rel="stylesheet" />

    <script type="text/javascript">
        NavBar = new __NavBar('Graphics');
    </script>
    
</head>

<body onload="Graphics.init()"> 
    
    <header>
        <?php require('Navbar.inc'); ?>
    </header>

    <section>
        <label for="classSelector">Класс:</label>
        <select id="classSelector">
            <?php fillClassSelector($ClassID); ?>
        </select>
        
        <div id="MainPlot"></div>
        <div id="legend"></div>
        <div>
            <input id="SA_CB" type="checkbox" onchange="Graphics.MultiCheck();" checked="checked"/>
            <label for="SA_CB">Включить/выключить всё</label>
        </div>
        
        <p style="margin-bottom:0;">Можно выделить дипазон для увеличения:</p>
        <div id="overview"></div>
    </section>
<!-- Yandex.Metrika counter --><div style="display:none;"><script type="text/javascript">(function(w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter10427686 = new Ya.Metrika({id:10427686, enableAll: true, ut:"noindex"}); } catch(e) { } }); })(window, "yandex_metrika_callbacks");</script></div><script src="//mc.yandex.ru/metrika/watch.js" type="text/javascript" defer="defer"></script><noscript><div><img src="//mc.yandex.ru/watch/10427686?ut=noindex" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter --> 
</body>
</html> 