<?php

define('IN_CONDUIT', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(ADMIN_LEVEL);
require_once('FillSelectors.inc');

?>
<!DOCTYPE HTML>
<html>
<head>

    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    
    <title>Загрузка данных</title>

    <!-- Подключаем движок -->
    <script type="text/javascript" src="js/UploadManager.js"></script>
    <link type="text/css" href="css/UploadManager.css" rel="stylesheet" />

    <!-- Подключаем jQuery и jQuery UI (Resizable) -->
    <script type="text/javascript" src="js/jquery-1.6.1.min.js"></script>
    <script type="text/javascript" src="js/jquery-ui-1.8.13.custom.min.js"></script>
    <link type="text/css" href="css/jquery.ui/theme.css" rel="stylesheet" />
    <link type="text/css" href="css/jquery.ui/resizable.css" rel="stylesheet" />
    <link type="text/css" href="css/jquery.ui/core.css" rel="stylesheet" />

    <!-- Подключаем jQuery Cookie plugin -->
    <script type="text/javascript" src="js/jquery.cookie.min.js"></script>
    <!-- Подключаем jQuery Form plugin -->
    <script type="text/javascript" src="js/jquery.form.min.js"></script>
    
    <!-- Подключаем панели инструментов -->
    <script type="text/javascript" src="js/Bars.js"></script>
    <link type="text/css" href="css/Bars.css" rel="stylesheet" />

    <script type="text/javascript">
        NavBar = new __NavBar('UploadManager');
    </script>
<style type="text/css">
<!--
body { color: #000000; background-color: #FFFFFF; }
.xml1-attributename { color: #808000; }
.xml1-attributevalue { color: #0000FF; }
.xml1-cdatasection { color: #996666; font-style: italic; }
.xml1-comment { color: #008000; font-style: italic; }
.xml1-doctypesection { color: #800000; font-style: italic; }
.xml1-elementname { color: #800080; }
.xml1-entityreference { color: #800000; }
.xml1-namespaceattributename { color: #808000; }
.xml1-namespaceattributevalue { color: #000080; }
.xml1-processinginstruction { color: #FF68FF; font-weight: bold; font-style: italic; }
.xml1-symbol { color: #800080; }
.xml1-text { color: #000000; }
.xml1-whitespace { color: #008080; font-style: italic; }
-->
</style>
</head>
</head>

<body onload="UploadManager.init()">
    
    <header>
        <?php require('Navbar.inc'); ?>
    </header>
    
    <form id="uploadForm" action="ajax/ParseXML.php" method="post"></form>
    
    <div id="typeSelector">
        Что будем грузить?<br />
        <input id="type_listok" type="radio" name="type" value="listok" form="uploadForm" onchange="UploadManager.changeType()" checked="checked"/>
        <label for="type_listok">Листок</label>
        <br />
        <input id="type_class" type="radio" name="type" value="class" form="uploadForm" onchange="UploadManager.changeType()" />
        <label for="type_class">Список класса</label>
    </div>
    
    <div id="classSelector" hidden='hidden'>
        Класс: 
        <select name="Class" form="uploadForm" onchange="UploadManager.selectClass()">
            <?php 
            if (isset($_COOKIE['UploadClass'])) {
                $ClassID = $_COOKIE['UploadClass'];
            } elseif (isset($_COOKIE['Class'])) {
                $ClassID = $_COOKIE['Class'];
            } else {
                unset($ClassID);
            }
            fillClassSelector($ClassID, true); 
            ?>
        </select>
    </div>

    
    <div>
        Введите XML:<br />
        <div>
            <code id="Ruler" hidden="hidden" data-size=1>1</code>
            <textarea id="XML" name="XML" form="uploadForm" required="required" 
                      rows="20" wrap="off" maxlength="100000" spellcheck="false"
                      onscroll="UploadManager.scrollRuler()"></textarea>
        </div>
    </div>
    
    <input type="submit" value="Отправить" form="uploadForm" />
    
    <div>
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />

        <p> Пример XML для листка:
<pre>
<code><span style="font: 10pt Courier New;"><span class="xml1-processinginstruction">&lt;?xml version='1.0'?&gt;
</span><span class="xml1-symbol">&lt;listok</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">number</span><span class="xml1-whitespace"> </span><span class="xml1-symbol">= '</span><span class="xml1-attributevalue">nn</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">description</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">List Name.</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">1</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">date</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">MM.YYYY</span><span class="xml1-symbol">'&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">1</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">0</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">1</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">2</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">0</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">2</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">3</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">0</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">3а</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">3</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">0</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">3б</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">3</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">0</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">3в</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">3</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">0</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">3г</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">3</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">1</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">3д</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">3</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">1</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">3е</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;problem</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">group</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">3</span><span class="xml1-symbol">'</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">type</span><span class="xml1-symbol">='</span><span class="xml1-attributevalue">2</span><span class="xml1-symbol">'&gt;</span><span class="xml1-text">3ж</span><span class="xml1-symbol">&lt;/problem&gt;
</span><span class="xml1-text"></span><span class="xml1-symbol">&lt;/listok&gt;

</span></span>
</code></pre>

        <p> Для задач type 0 - обычная, 1 - со звёздочкой, 2 - с двумя звёздочками; Для листка type 1 - обычный, 2 - дополнительный.
     </div>    

    <div>
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />

        <p> Пример XML для класса:
<pre>
<code><span style="font: 10pt Courier New;"><span class="xml1-processinginstruction">&lt;?xml version=&quot;1.0&quot;?&gt;
</span><span class="xml1-symbol">&lt;class</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">name</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">test</span><span class="xml1-symbol">&quot;</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">description</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">test class</span><span class="xml1-symbol">&quot;&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 1 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 1</span><span class="xml1-symbol">&lt;/pupil&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 2 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 2</span><span class="xml1-symbol">&lt;/pupil&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 3 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 3</span><span class="xml1-symbol">&lt;/pupil&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 4 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 4</span><span class="xml1-symbol">&lt;/pupil&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 5 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 5</span><span class="xml1-symbol">&lt;/pupil&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 6 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 6</span><span class="xml1-symbol">&lt;/pupil&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 7 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 7</span><span class="xml1-symbol">&lt;/pupil&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 8 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 8</span><span class="xml1-symbol">&lt;/pupil&gt;
</span><span class="xml1-text">  </span><span class="xml1-symbol">&lt;pupil</span><span class="xml1-whitespace"> </span><span class="xml1-attributename">nick</span><span class="xml1-symbol">=&quot;</span><span class="xml1-attributevalue">Pupil 9 Nick</span><span class="xml1-symbol">&quot;&gt;</span><span class="xml1-text">Test Pupil 9</span><span class="xml1-symbol">&lt;/pupil&gt;
&lt;/class&gt;
</span></span>
</code></pre>
     </div>    

<!-- Yandex.Metrika counter --><div style="display:none;"><script type="text/javascript">(function(w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter10427686 = new Ya.Metrika({id:10427686, enableAll: true, ut:"noindex"}); } catch(e) { } }); })(window, "yandex_metrika_callbacks");</script></div><script src="//mc.yandex.ru/metrika/watch.js" type="text/javascript" defer="defer"></script><noscript><div><img src="//mc.yandex.ru/watch/10427686?ut=noindex" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->
</body>
</html>