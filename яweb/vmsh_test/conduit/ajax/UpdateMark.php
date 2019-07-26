<?php

define('IN_CONDUIT', true);
define('AJAX', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(TEACHER_LEVEL);
require_once('AjaxError.inc');

?>
<?php

// Здесь есть уязвимость: не проверяется, что пользователь имеет доступ к классу, который обновляет

$Request = json_decode($_POST['Request'], true);
$L = count($Request);
if ($L == 0) {
    echo '[]';
    exit(0);
}

if ($_POST['Type'] === 'update') {
    
    $Amendment  = array('U' => $USERDISPLAYNAME,
                        'T' => strftime('%Y-%m-%d %T'));
    
    // Собираем список вставляемых значений и сразу ответ
    for ($i = 0; $i < $L; $i++) {
        $Rows[$i] = '(' . 
                         mysql_real_escape_string($Request[$i]['Pupil']) . ', ' .
                         mysql_real_escape_string($Request[$i]['Problem']) . ', ' .
                         '"' . mysql_real_escape_string($Request[$i]['Mark']) . '", ' .
                         '"' . $USERNAME . '"' .
                    ')';
        $Response[$i] = array('Pupil'       => $Request[$i]['Pupil'],
                              'Problem'     => $Request[$i]['Problem'],
                              'Text'        => filter_var($Request[$i]['Mark'], FILTER_SANITIZE_SPECIAL_CHARS),
                              'Amendment'   => $Amendment);
    }
    
    // Добавляем записи в базу
    $sql = 'INSERT INTO `PResult` (`PupilID`, `ProblemID`, `Mark`, `User`) 
                   VALUES ' . implode(',', $Rows) .
            ' ON DUPLICATE KEY UPDATE `Mark` = VALUES(`Mark`), `User` = VALUES(`User`)';
    $result = mysql_query($sql);
    if (!$result) {
        triggerAjaxError(500);
    }

    // Добавляем записи в историю
    $sql = 'INSERT INTO `PResultHistory` (`PupilID`, `ProblemID`, `Mark`, `User`) 
                   VALUES ' . implode(',', $Rows);
    $result = mysql_query($sql);
    if (!$result) {
        triggerAjaxError(500);
    }
    
    echo json_encode($Response);    

} elseif ($_POST['Type'] === 'rollback') {
    $sql = 'START TRANSACTION';
    if(!mysql_query($sql)) {
        triggerAjaxError(500);
    }
    
    // Для каждой из ячеек делаем следующее:
        // Если последнее изменение сделано текущим пользователем, то:
            // Вытаскиваем из истории предыдущее состояние
            // Прописываем его в PResult
            // Удаляем отменённую операцию из истории
    $Response = array();
    try {
        for ($i = 0; $i < $L; $i++) {
            $sql = 'SELECT `PResultHistory`.`Mark`, `PResultHistory`.`User`, `PResultHistory`.`TS`, 
                            COALESCE(`PUser`.`DisplayName`, `PResultHistory`.`User`) AS `DisplayName`
                        FROM `PResultHistory` LEFT JOIN `PUser` 
                                              ON `PResultHistory`.`User` = `PUser`.`User` 
                        WHERE   `PupilID` = "' . $Request[$i]['Pupil'] . '" AND 
                                `ProblemID` = "' . $Request[$i]['Problem'] . '" 
                        ORDER BY `TS` DESC LIMIT 2';
            $result = mysql_query($sql);
            if(!$result) {
                throw new Exception('SQL error');
            }
            $LastAmend = mysql_fetch_assoc($result);
            if(!$LastAmend) { // Изменений вообще не было; запрос ошибочный
                continue;
            }
            if($LastAmend['User'] !== $USERNAME) { // Последнее изменение сделал кто-то другой; откат не нужен
                continue;
            }
            $PrevAmend = mysql_fetch_assoc($result); // Предыдущее состояние метки
            if(!$PrevAmend) { // До этого метки не было вообще. Просто её удаляем
                $sql = 'DELETE FROM `PResult` 
                        WHERE   `PupilID` = "' . $Request[$i]['Pupil'] . '" AND 
                                `ProblemID` = "' . $Request[$i]['Problem'] . '" AND
                                `User` = "' . $USERNAME . '"'; 
                $result = mysql_query($sql);
                if(!$result) {
                    throw new Exception('SQL error');
                }
                $sql = 'DELETE FROM `PResultHistory` 
                        WHERE   `PupilID` = "' . $Request[$i]['Pupil'] . '" AND 
                                `ProblemID` = "' . $Request[$i]['Problem'] . '" AND
                                `User` = "' . $USERNAME . '"'; 
                $result = mysql_query($sql);
                if(!$result) {
                    throw new Exception('SQL error');
                }
                $Response[]   = array('Pupil'       => $Request[$i]['Pupil'],
                                      'Problem'     => $Request[$i]['Problem'],
                                      'Text'        => '');
            } else { // Метка была. Восстанавливаем её состояние
                $sql = 'UPDATE `PResult` 
                        SET     `Mark` = "' . $PrevAmend['Mark'] . '",
                                `TS`   = "' . $PrevAmend['TS'] . '",
                                `User` = "' . $PrevAmend['User'] . '" 
                        WHERE   `PupilID` = "' . $Request[$i]['Pupil'] . '" AND 
                                `ProblemID` = "' . $Request[$i]['Problem'] . '" AND
                                `User` = "' . $USERNAME . '"'; 
                $result = mysql_query($sql);
                if(!$result) {
                    throw new Exception('SQL error');
                }
                $sql = 'DELETE FROM `PResultHistory` 
                        WHERE   `PupilID` = "' . $Request[$i]['Pupil'] . '" AND 
                                `ProblemID` = "' . $Request[$i]['Problem'] . '" AND
                                `User` = "' . $USERNAME . '" AND
                                `TS` = "' . $LastAmend['TS'] . '"'; 
                $result = mysql_query($sql);
                if(!$result) {
                    throw new Exception('SQL error');
                }
                $Amendment    = array('U'           => $PrevAmend['DisplayName'],
                                      'T'           => $PrevAmend['TS']);
                $Response[]   = array('Pupil'       => $Request[$i]['Pupil'],
                                      'Problem'     => $Request[$i]['Problem'],
                                      'Text'        => filter_var($PrevAmend['Mark'], FILTER_SANITIZE_SPECIAL_CHARS),
                                      'Amendment'   => $Amendment);
            }
        }
        $sql = 'COMMIT';
        if(!mysql_query($sql)) {
            throw new Exception('SQL error');
        }
    } catch (Exception $e) {
        $sql = 'ROLLBACK';
        @mysql_query($sql);
        triggerAjaxError(500);
    }
    echo json_encode($Response);
}
?>