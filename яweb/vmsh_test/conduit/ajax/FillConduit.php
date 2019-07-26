<?php

define('IN_CONDUIT', true);
define('AJAX', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(PUPIL_LEVEL);
require_once('AjaxError.inc');

?>
<?php

function fillConduit($ClassID, $ListID) {
    global $db;
    $ProblemOrderBy = '`PProblem`.`Number`, `PProblem`.`Name`, `PProblem`.`ID`';
    $PupilOrderBy = '`PPupil`.`Name1`, `PPupil`.`Name2`, `PPupil`.`Name3`, `PPupil`.`ID`';
    
    // Готовим массив школьников
    $Pupils = array();
    $sql = 'SELECT 
                PPupil.ID as I, 
                PPupil.Name1 as S, PPupil.Name2 as N, PPupil.Name3 as P, 
                PPupil.Nick as A
            FROM PPupil
            WHERE
                PPupil.ClassID = ' . $ClassID . '
            ORDER BY 
                ' . $PupilOrderBy . '
           ';
    $result = mysql_query($sql);
    while ($row = mysql_fetch_assoc($result)) {
        $Pupils[] = $row;
    }
    
    // Готовим массив задач
    $Problems = array();
    $sql = 'SELECT 
                `PProblem`.`ID` as I, `PProblem`.`Group` as G, 
                CONCAT(`PProblem`.`Name`, `PProblemType`.`Sign`) as N,
                TRIM(`PProblemType`.`Sign`) as S
            FROM `PProblem` INNER JOIN `PProblemType`
                 ON `PProblem`.`ProblemTypeID` = `PProblemType`.`ID`
            WHERE 
                `PProblem`.`ListID` = ' . $ListID . '
            ORDER BY
                ' . $ProblemOrderBy . ' 
           ';
    $result = mysql_query($sql);
    while ($row = mysql_fetch_assoc($result)) {
        $Problems[] = $row;
    }
    
    // Готовим массив отметок
    $Marks = array();
    $sql = 'SELECT 
                PResult.PupilID as PupilID, PResult.ProblemID as ProblemID, 
                PResult.Mark as Text, 
                COALESCE(PUser.DisplayName, PResult.User) as User, PResult.TS as DateTime
            FROM PResult INNER JOIN PPupil
                 ON PResult.PupilID = PPupil.ID 
                         INNER JOIN PProblem
                 ON PResult.ProblemID = PProblem.ID
                         LEFT JOIN PUser
                 ON PResult.User = PUser.User
            WHERE
                PPupil.ClassID = ' . $ClassID . ' AND PProblem.ListID = ' . $ListID . '
           ';
    $result = mysql_query($sql);
    while ($row = mysql_fetch_assoc($result)) {
        $key = $row['PupilID'] . ':' . $row['ProblemID'];
        $Amendment['U']      = $row['User'];
        $Amendment['T']  = $row['DateTime'];
        $mark['T']           = $row['Text'];
        $mark['A']      = $Amendment;
        $Marks[$key]            = $mark;
    }
    
    // Собираем всё воедино
    $Response['P']         = $Pupils;
    $Response['T']       = $Problems;
    $Response['M']          = $Marks;
    
    echo json_encode($Response);
}

// Защита от SQL-инъекции
$ClassID = (string)mysql_real_escape_string($_POST['Class']);
$ListID  = (string)mysql_real_escape_string($_POST['List']);

try {
    fillConduit($ClassID, $ListID);
} catch (Exception $e) {
    triggerAjaxError(404);
}

?>