<?php

if(isset($_POST['submit']))
{
    
    # Сравниваем пароли
    if("179" === $_POST['password'] and "vmsh_test" === $_POST['login'])
    {
        # Генерируем хеш для куки
        # $hash = md5('vmsh_test'.md5($_SERVER['REMOTE_ADDR']));
        
        # Ставим куки
        setcookie("in_vmsh", md5('in_vmsh'), time()+60*60*24*30, "/vmsh_test/");
        # Ставим куки
        setcookie("cond", md5('cond'), time()+60*60*24*30, "/vmsh_test/");
        
        # Переадресовываем браузер туда, куда мы и так собирались
        header("Location: http://".$_SERVER['SERVER_NAME'].$_SERVER['REQUEST_URI']); exit();
    } elseif ("guest" === $_POST['password'] and "vmsh_test" === $_POST['login']){
        # Ставим куки
        setcookie("in_vmsh", md5('in_vmsh'), time()+60*60*24*30, "/vmsh_test/");
        
        # Переадресовываем браузер туда, куда мы и так собирались
        header("Location: http://".$_SERVER['SERVER_NAME'].$_SERVER['REQUEST_URI']); exit();
    } elseif ("Shashkov" === $_POST['password'] and "admin" === $_POST['login']){
        # Ставим куки
        setcookie("in_vmsh", md5('in_vmsh'), time()+60*60*24*30, "/vmsh_test/");
        # Ставим куки
        setcookie("cond", md5('cond'), time()+60*60*24*30, "/vmsh_test/");
        # Ставим куки
        setcookie("admin", md5('admin57'), time()+60*60*24*30, "/vmsh_test/");
        
        # Переадресовываем браузер туда, куда мы и так собирались
        header("Location: http://".$_SERVER['SERVER_NAME'].$_SERVER['REQUEST_URI']); exit();
    } else
    {
        setcookie("hash", "", time()+1, "/vmsh_test/");
        print "Вы ввели неправильный логин/пароль";
    }
}
?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
  <title>Login</title>
	<style>
    html, body {height:100%;margin:0;}
	</style>  
</head>
<body>
<table style="width: 100%; height: 100%; text-align: center;"><tr><td style="text-align: center; vertical-align: middle;">
<form method="POST" style="width: 200px; margin: 0 auto;">
<table>
<tr><td>Login</td><td> <input name="login" type="text"></td></tr>
<tr><td>Password</td><td> <input name="password" type="password"></td></tr>
<tr><td colspan="2" style="text-align: center;"><input name="submit" type="submit" value="Enter"></td></tr>
</table>
</form>
</td></tr></table>
</body>
