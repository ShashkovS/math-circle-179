<?php
// Скрипт проверки


if (isset($_COOKIE['in_vmsh']))
{   
    # Генерируем хеш для куки
    # $hash = md5('vmsh_test'.md5($_SERVER['REMOTE_ADDR']));

    if(md5('in_vmsh') !== $_COOKIE['in_vmsh']) 
    {
        # header("Location: login.php"); exit();
        require_once('login.php'); exit();
    }
    else
    {
        # Всё ОК
    }
}
else
{
    # header("Location: login.php"); exit();
    require_once('login.php'); exit();
} 
?>