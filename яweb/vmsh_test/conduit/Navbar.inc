<?php

if (!defined('IN_CONDUIT')){
    // Попытка прямого доступа к файлу
    exit();
}

?>
        <nav class="bar navbar">
            <ul>
                <li class="user">
                    <span class="currentUser">&#9662;&nbsp;<?php echo $USERNAME;?></span>
                    <div>
                    <ul>
                        <li onclick="NavBar.relogin()">Зайти под другим именем</li>
                        <li onclick="NavBar.logout()">Выйти</li>
                    </ul>
                    </div>
                </li>
                <li id="Conduit" class="tab"><a href="Conduit.php">Кондуит</a></li>
                <?php if ($USERLEVEL >= ADMIN_LEVEL) echo 
                '<li id="UploadManager" class="tab"><a href="UploadManager.php">Загрузка данных</a></li>
';?>
                <li id="Graphics" class="tab"><a href="Graphics.php">Графики</a></li>
                <li id="News" class="tab"><a href="News.php">Новости</a></li>
                <li id="About" class="tab"><a href="About.php">О проекте</a></li>
                <li id="FAQ" class="tab"><a href="FAQ.php">Справка</a></li>
            </ul>
        </nav>
