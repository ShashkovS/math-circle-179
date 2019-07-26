<?php

define('IN_CONDUIT', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(PUPIL_LEVEL);

?>
<!DOCTYPE HTML>

<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    
    <title>Справка</title>
    
    <!-- Подключаем jQuery -->
    <script type="text/javascript" src="js/jquery-1.6.1.min.js"></script>
    
    <!-- Подключаем панели инструментов -->
    <script type="text/javascript" src="js/Bars.js"></script>
    <link type="text/css" href="css/Bars.css" rel="stylesheet" />

    <script type="text/javascript">
        NavBar = new __NavBar('FAQ');
    </script>
    
</head>

<body onload="NavBar.init()"> 
    
    <header>
        <?php require('Navbar.inc'); ?>
    </header>

    <section>
        <ul style="list-style-type: none;">
            <li  class="Q">Q: А где же справка?</li>
            <li  class="A">A: Когда-нибудь будет.</li>
        </ul>
    </section>
<!-- Yandex.Metrika counter --><div style="display:none;"><script type="text/javascript">(function(w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter10427686 = new Ya.Metrika({id:10427686, enableAll: true, ut:"noindex"}); } catch(e) { } }); })(window, "yandex_metrika_callbacks");</script></div><script src="//mc.yandex.ru/metrika/watch.js" type="text/javascript" defer="defer"></script><noscript><div><img src="//mc.yandex.ru/watch/10427686?ut=noindex" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->
</body>
</html> 