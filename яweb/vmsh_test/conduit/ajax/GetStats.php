<?php

define('IN_CONDUIT', true);
define('AJAX', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(PUPIL_LEVEL);
require_once('AjaxError.inc');

?>
<?php

function getStats($ClassID) {
    global $db;
    
    $sql = 'SELECT  TRIM(CONCAT(`PPupil`.`Name1`," ",`PPupil`.`Name2`," ",`PPupil`.`Name3`)) AS `FIO`, 
                    CONCAT(SUBSTR(`PResult`.`Mark`,7,4), SUBSTR(`PResult`.`Mark`,4,2), SUBSTR(`PResult`.`Mark`,1,2)) AS `Date`,
                    COUNT(*) AS `Solved` 
                FROM `PResult`  LEFT JOIN `PPupil` 
                                ON `PResult`.`PupilID` = `PPupil`.`ID`
                WHERE   `PPupil`.`ClassID` = ' . $ClassID . ' 
                        AND `PResult`.`Mark` LIKE "__/__/____" 
                GROUP BY `PResult`.`PupilID`, `PResult`.`Mark`
                ORDER BY 1,2';

    $Dates = array();
    $Pupils = array();

    // Запоминаем все ненулевые результаты школьников и какие даты вообще бывают.
    $result = mysql_query($sql);
    while ($row = mysql_fetch_assoc($result)) {
        $Pupils[$row['FIO']][$row['Date']] = (int)$row['Solved'];
        if (!in_array($row['Date'], $Dates)) {
            $Dates[] = $row['Date'];
        }
    }
    
    // Сортируем даты по возрастанию
    sort($Dates);
    
    // Добавляем нулевые значения для школьников и сортируем их результаты
    foreach ($Pupils as &$Pupil) {
        foreach ($Dates as $Date) {
            if (!isset($Pupil[$Date])) {
                $Pupil[$Date] = 0;
            }
        }
        ksort($Pupil);
        $Pupil = array_values($Pupil);
    }
    
    // Собираем всё воедино
    $Response['D'] = $Dates;
    $Response['P'] = $Pupils;
    
    echo json_encode($Response);
}

// Защита от SQL-инъекции
$ClassID = (string)mysql_real_escape_string($_POST['Class']);

try {
    getStats($ClassID);
} catch (Exception $e) {
    triggerAjaxError(404);
}

?>