<?php
if(isset($_POST['submit']))
{
    if (strpos($_SERVER['SCRIPT_NAME'], '-a') !== false) { 
      $vm_sh_login = 'c179';
      $vm_sh_password = 'cube';
    } else {
      $vm_sh_login = 'c179';
      $vm_sh_password = 'cube';
    }

    # Сравниваем пароли
    if($vm_sh_password === $_POST['password'] and $vm_sh_login === $_POST['login'])
    {
        # Ставим куки
        setcookie("in_vmsh", md5('in_vmsh'), time()+60*60*24*30, "/vmsh_test/");
        # Ставим куки
        setcookie("cond", md5('cond'), time()+60*60*24*30, "/vmsh_test/");
        # Переадресовываем браузер туда, куда мы и так собирались
        header("Location: //".$_SERVER['SERVER_NAME'].$_SERVER['REQUEST_URI']); exit();
    } elseif ("???somePassword" === $_POST['password'] and "admin" === $_POST['login']){
        # Ставим куки
        setcookie("in_vmsh", md5('in_vmsh'), time()+60*60*24*30, "/vmsh_test/");
        # Ставим куки
        setcookie("cond", md5('cond'), time()+60*60*24*30, "/vmsh_test/");
        # Ставим куки
        setcookie("admin", md5('admin57'), time()+60*60*24*30, "/vmsh_test/");
        # Переадресовываем браузер туда, куда мы и так собирались
        header("Location: //".$_SERVER['SERVER_NAME'].$_SERVER['REQUEST_URI']); exit();
    }	
 else
    {
        setcookie("hash", "", time()+1, "/vmsh_test/");
    }
}
?>
<?php define('IN_VMSH', true);?>



<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="keywords" content="VMSH">
  <meta name="description" content="VMSH">
  <title>ВМШ 2018-2019, 5, 6 класс, 179 школа</title>
  <link rel="stylesheet" href="https://www.shashkovs.ru/vmsh_test/c/vm-sh.min.css">
  <script src="https://www.shashkovs.ru/vmsh_test/c/vm-sh.min.js"></script>
  <script src="https://yastatic.net/jquery/2.1.4/jquery.min.js"></script>
  <script>
    $( document ).ready(window.Conduit.init);
  </script>
  <?php if (((isset($_COOKIE['admin']) && md5('admin57') === $_COOKIE['admin'])) or (isset($_GET["show_secret_stat"]))){ echo(
<<<ARTICLE
  <script type="text/javascript">
  function show_stat() {
    $('.stat').css('display', 'inline');
  }
  window.onload = show_stat;
  </script>
ARTICLE
  );}?>
</head>

<body>
  <div id="layout">
    <div id="header">
      <div class="n-left-corner"></div>
      <div class="n-center">
        <ul>
          <li>
            <?php if (strpos($_SERVER['SCRIPT_NAME'], '-a') !== false) { 
              echo('<a href="../vmsh_test/">Начинающим</a>'); 
            } else {
              echo('<a href="../vmsh-a_test/">Продолжающим</a>'); 
            }
            ?>
          </li>
          <li>
            <a href="about.html">О&nbsp;ВМШ</a>
          </li>
          <li>
            <a href="contact.html">Контакты</a>
          </li>
          <li>
            <a href="https://179.ru/" target="_blank">Сайт школы</a>
          </li>
        </ul>
      </div>
      <div class="n-right-corner"></div>
    </div>



      <div class="b-first">
            <?php require("onTheTopForAll.html");?>
      </div>

    <div id="content">
      <?php 
        require_once('dates.inc');
        $days =  array("", "понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье");
        $month =  array("", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря");
        $curdt = new DateTime;
        $weekdt = new DateTime;
        $prev = "";
        reset($datesarr);
        foreach ($datesarr as $number => $lesdt) {
          if ($lesdt->format('Y-m-d H:i:s') <= $curdt->format('Y-m-d H:i:s')) {
            break;
          }
          $prev = $number;
        }
        $lesdt = $datesarr[$prev];
        if ($lesdt) {
          $textdt = $days[(int)($lesdt->format('N'))]." ".$lesdt->format('j')." ".$month[(int)($lesdt->format('m'))];
          echo(
<<<ARTICLE
      <div class="b-first">
          <div class="lesson b-second">
            <h2 class="lesson_title">Ближайшее занятие ВМШ для 5 и 6 классов в 179-й школе состоится {$textdt} в 16:40.</h2>
          </div>
      </div>
ARTICLE
          );
        }        
        # админу можно всё ;-)
        if (isset($_COOKIE['admin']) && md5('admin57') === $_COOKIE['admin']) {
          $curdt->modify('+1000 day');
          $weekdt->modify('+1000 day');
        } elseif (isset($_COOKIE['cond']) && md5('cond') === $_COOKIE['cond']) {
          $weekdt->modify('-7 day');
        } else {
          $weekdt = new DateTime("2016-09-21T19:00:00Z");
          # $curdt->modify('-28 day');
        }
      ?>
      


      <?php
        if ((isset($_COOKIE['admin']) && md5('admin57') === $_COOKIE['admin']) || (isset($_COOKIE['cond']) && md5('cond') === $_COOKIE['cond'])) {
          echo('<div class="b-first">');
          require("onTheTopForReg.html");
          echo('</div>');
        } else {
          echo(
<<<ARTICLE
      <div class="b-first">
          <div class="lesson b-second">
            <section class="lesson_data">
              <h2 class="lesson_title">Я знаю логин и пароль!</h2>
              <form method="POST" style="width: 200px; margin: 0 auto;">
              <table>
              <tr><td>Login</td><td> <input name="login" type="text"></td></tr>
              <tr><td>Password</td><td> <input name="password" type="password"></td></tr>
              <tr><td colspan="2" style="text-align: center;"><input name="submit" type="submit" value="Enter"></td></tr>
              </table>
              </form>
            </section>
          </div>
          </div>
      </div>
ARTICLE
          );
          echo('<div class="b-first">');
          require("onTheTopForNoReg.html");
          if (strpos($_SERVER['SCRIPT_NAME'], '-a') !== false) { 
              require("onTheTopForPro.html"); 
          } else {
              require("onTheTopForBeg.html");
          }
          echo('</div>');
        }
      ?>

      <div class="b-first">
      <?php 
        reset($datesarr);
        foreach ($datesarr as $number => $lesdt) {
          if ($lesdt->format('Y-m-d H:i:s') <= $curdt->format('Y-m-d H:i:s') && file_exists("data/{$number}-lesson.html")) {
            $i = (int)($number);
            $textdt = $lesdt->format('j')." ".$month[(int)($lesdt->format('m'))]." ".$lesdt->format('Y')." г.";
            echo(
<<<ARTICLE
<div class="lesson b-second" id="$number">
  <h2 class="lesson_title">Занятие {$i}. 
    <a href="#{$number}">#</a>
    <a class="inPDF" href="data/{$number}-lesson.pdf">pdf</a>
    <span class="lesDate">{$textdt}</span>
    
  </h2>
<div class="lesson_data">
ARTICLE
            );
            include "data/{$number}-lesson.html";
            echo(
<<<ARTICLE
</div>
ARTICLE
            );
            if ($lesdt->format('Y-m-d H:i:s') <= $weekdt->format('Y-m-d H:i:s')) {
              echo(
<<<ARTICLE
<!--<div class="lesson_solution">
  <img class="spooler_img" src="//www.shashkovs.ru/vmsh_test/c/dw.gif" alt=""/><span class="spooler solution_spooler">Решения задач</span>
  <div class="solution_container nodisplay"><p>Подождите, решения загружаются.</p></div>
</div>-->
ARTICLE
              );
            }
            if (isset($_COOKIE['cond']) && md5('cond') === $_COOKIE['cond']) {
              echo(
<<<ARTICLE
<div class="lesson_conduit">
  <img class="spooler_img" src="//www.shashkovs.ru/vmsh_test/c/dw.gif" alt=""/><span class="spooler conduit_spooler">Кондуит</span>
  <div class="conduit_container nodisplay"><p>Ждите. Производится загрузка данных с сервера&hellip;</p></div>
</div>
ARTICLE
              );
            }
            echo('</div>');
          }
        }
      ?>
      </div>
    </div>


    <div id="footer">
    </div>

  </div>

<!-- Yandex.Metrika counter --><script type="text/javascript"> (function (d, w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter32473920 = new Ya.Metrika({ id:32473920, clickmap:true, trackLinks:true, accurateTrackBounce:true }); } catch(e) { } }); var n = d.getElementsByTagName("script")[0], s = d.createElement("script"), f = function () { n.parentNode.insertBefore(s, n); }; s.type = "text/javascript"; s.async = true; s.src = "https://mc.yandex.ru/metrika/watch.js"; if (w.opera == "[object Opera]") { d.addEventListener("DOMContentLoaded", f, false); } else { f(); } })(document, window, "yandex_metrika_callbacks");</script><noscript><div><img src="https://mc.yandex.ru/watch/32473920" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->
</body>
</html>