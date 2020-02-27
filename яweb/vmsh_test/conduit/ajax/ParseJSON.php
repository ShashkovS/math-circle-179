<?php
define('IN_CONDUIT', true);
define('AJAX', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
//checkAccess(TEACHER_LEVEL);
require_once('AjaxError.inc');
require_once('FillSelectors.inc');
?>
<?php
$Response['yes'] = 'Yes!';

// Обрабатываем запрос
try {
    $obj = json_decode(file_get_contents('php://input'));
    foreach ($obj->lists as $list) {
        $sql='delete from `PList` where `Number` = "' . mysql_real_escape_string($list->Number) . '"';
        mysql_query($sql);
        $sql = 'INSERT INTO `PList` (`ListTypeID`, `ClassID`, `Number`, `Description`, `Date`) VALUES 
                (' . mysql_real_escape_string($list->ListTypeID) . ',
                 ' . mysql_real_escape_string($list->ClassID) . ',
                "' . mysql_real_escape_string($list->Number) . '",
                "' . mysql_real_escape_string($list->Description) . '",
                "' . mysql_real_escape_string($list->Date) . '")';
        if(!mysql_query($sql)) {
            echo mysql_error();
            throw new Exception('Could not insert listok into database: ' . mysql_error());
        }
        $ListID = mysql_insert_id();    // узнаём ID добавленной записи        
        foreach ($list->problems as $problem) {
            $sql = 'INSERT INTO `PProblem` (`ProblemTypeID`, `ListID`, `Number`, `Group`, `Name`) VALUES 
                    (' . mysql_real_escape_string($problem->ProblemTypeID) . ',
                     ' . $ListID . ',
                     ' . mysql_real_escape_string($problem->Number) . ',
                     ' . mysql_real_escape_string($problem->Group) . ',
                    "' . mysql_real_escape_string($problem->Name) . '")';
            if(!mysql_query($sql)) {
                throw new Exception('Could not insert problem into database: ' . mysql_error());
            }
        }
    }
    foreach ($obj->pupils as $pupil) {
        $sql = 'insert into PPupil (`ClassID`, `Name1`, `Name2`, `xlsID`) VALUES
                (' . mysql_real_escape_string($pupil->ClassID) . ',
                "' . mysql_real_escape_string($pupil->Name1) . '",
                "' . mysql_real_escape_string($pupil->Name2) . '",
                "' . mysql_real_escape_string($pupil->xlsID) . '") 
                on DUPLICATE KEY UPDATE Name1=VALUES(Name1), Name2=VALUES(Name2)';
        if(!mysql_query($sql)) {
            throw new Exception('Could not insert problem into database: ' . mysql_error());
        }
    }
    foreach ($obj->marks as $mark) {
        $sql = 'call PutPlus
                ("' . mysql_real_escape_string($mark->LN) . '",
                 "' . mysql_real_escape_string($mark->PN) . '",
                 "' . mysql_real_escape_string($mark->PI) . '")';
        if(!mysql_query($sql)) {
            throw new Exception('Could not insert problem into database: ' . mysql_error());
        }
    }
    $Response['code']    = 0;
    $Response['message'] = 'Done!';
} catch (Exception $e) {
    $Response['code']    = 1;
    $Response['message'] = 'Upload process failed. ' . $e->getMessage().$sql;
}

// Возвращаем ответ
echo json_encode($Response);
?>