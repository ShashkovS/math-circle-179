<?php

if (!defined('IN_CONDUIT')){
    // Попытка прямого доступа к файлу
    exit();
}
require_once('Connect.inc');

?>
<?php

function classDisplayName($name, $description) {
    return filter_var($name, FILTER_SANITIZE_SPECIAL_CHARS);
}

function listDisplayName($number, $description) {
    return filter_var($number . ' - ' . $description, FILTER_SANITIZE_SPECIAL_CHARS);
}

function compareList(&$a, &$b) {
    return (int)($a['Text']) - (int)($b['Text']);
}

function fillClassSelector(&$ClassID, $allowNull = false) {
    global $db;
    if ($allowNull) {
        if (!isset($ClassID)) {
            $ClassID = 'NULL';
        }
        echo '<option value="NULL"';
        if ($ClassID === 'NULL') {
            echo ' selected="selected"';
        }
        echo '>';
        echo 'Все классы';
        echo '</option>';
    }
    
    // Формируем список доступных классов на основе таблицы PClass
    // Для уровня доступа Admin доступны все классы; для остальных права проверяются по таблице PUserClass
    global $USERLEVEL, $USERNAME;
    if ($USERLEVEL >= ADMIN_LEVEL) {
        $sql = 'SELECT `ID`, `Name`, `Description` FROM `PClass`';
    } else {
        $sql = 'SELECT `ID`, `Name`, `Description` FROM `PClass` INNER JOIN `PUserClass` ' . 
                    'ON `PClass`.`ID` = `PUserClass`.`ClassID` ' .
                    'WHERE `PUserClass`.`User` = "' . $USERNAME . '"';
    }
    $result = mysql_query($sql);
    $NotFound = true;
    $i = 0;
    while ($row = mysql_fetch_array($result)) {
        $Text = classDisplayName($row['Name'], $row['Description']);
        $ID = $row['ID'];
        if ($ClassID === $ID) {
            $Selected = true;
            // Запрошенный класс действительно присутствует в списке
            $NotFound = false;
        } else {
            $Selected = false;
        }
        $List[$i++] = array('ID'        => $ID,
                            'Text'      => $Text,
                            'Selected'  => $Selected);
    }
    
    if ($NotFound) {
        if ($i) {
            $List[0]['Selected'] = true;
            $ClassID = $List[0]['ID'];
        } else {
            $ClassID = 0;
            return;
        }
    }
    
    // Формируем html-код
    foreach ($List as &$Entry) {
        echo '<option value="' . $Entry['ID'] . '"';
        if ($Entry['Selected']) {
            echo ' selected="selected"';
        }
        echo '>' . $Entry['Text'] . '</option>';
    }
}

function fillListSelector(&$ListID, $ClassID) {
    global $db;
    
    if ($ClassID == 0) {
        $ListID = 0;
        return;
    }
    
    // Формируем список доступных листков на основе таблицы PList
    $sql = 'SELECT `ID`, `Number`, `Description` FROM `PList` ' . 
           'WHERE `ClassID`  = "' . $ClassID . '" OR `ClassID` IS NULL';
    $result = mysql_query($sql);
    $NotFound = true;
    $i = 0;
    while ($row = mysql_fetch_array($result)) {
        $Text = listDisplayName($row['Number'], $row['Description']);
        $ID = $row['ID'];
        if ($ListID === $ID) {
            $Selected = true;
            // Запрошенный листок действительно присутствует в списке
            $NotFound = false;
        } else {
            $Selected = false;
        }
        $List[$i++] = array('ID'        => $ID,
                            'Text'      => $Text,
                            'Selected'  => $Selected);
    }
    
    // Сортируем листки интеллектуально
    usort($List, 'compareList');
    
    if ($NotFound) {
        if ($i) {
            $List[0]['Selected'] = true;
            $ListID = $List[0]['ID'];
        } else {
            $ListID = 0;
            return;
        }
    }
    
    // Формируем html-код
    foreach ($List as &$Entry) {
        echo '<option value="' . $Entry['ID'] . '"';
        if ($Entry['Selected']) {
            echo ' selected="selected"';
        }
        echo '>' . $Entry['Text'] . '</option>';
    }
}
?>