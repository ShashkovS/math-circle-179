<?php

define('IN_CONDUIT', true);
define('AJAX', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(TEACHER_LEVEL);
require_once('AjaxError.inc');
require_once('FillSelectors.inc');

?>
<?php

class TProblem {
    public $number;
    public $type;
    public $name;
    public $group;
    
    private static $typesArray;
    
    function __construct(DOMElement $node, $internalNumber) {
        global $db;
        if ($node->tagName !== 'problem'){
            throw new Exception('Tag name not equal to \'problem\'');
        }
        $this->number = (int)$internalNumber;
        $this->name = mysql_real_escape_string($node->textContent);
        $this->type = (int)($node->getAttribute('type'));
        if (!self::checkType($this->type)) {
            throw new Exception('Invalid problem type');
        }
        $this->group = (int)($node->getAttribute('group'));
    }
    
    function write2SQL($ListID) {
        global $db;
        $sql = 'INSERT INTO `PProblem` (`ProblemTypeID`, `ListID`, `Number`, `Group`, `Name`) VALUES 
                (' . $this->type . ',
                 ' . $ListID . ',
                 ' . $this->number . ',
                 ' . $this->group . ',
                "' . $this->name . '")';
        if(!mysql_query($sql)) {
            throw new Exception('Could not insert problem into database: ' . mysql_error());
        }
    }
    
    static function checkType($t) {
        global $db;
        if (!isset(self::$typesArray)) {
            $sql = 'SELECT `ID` FROM `PProblemType`';
            $result = mysql_query($sql);
            if(!$result) {
                throw new Exception('Selection error: ' . mysql_error());
            }
            while ($row = mysql_fetch_array($result)) {
                self::$typesArray[] = (int)$row['ID'];
            }
        }
        return in_array($t, self::$typesArray, true);
    }
}

class TListok {
    public $number;
    public $type;
    public $description;
    public $date;
    public $problems;
    public $problemCount;
    public $class;
    
    private static $typesArray;
    
    function __construct(DOMElement $node, $class) {
        global $db;
        // Инициализируем сам листок
        if ($node->tagName !== 'listok'){
            throw new Exception('Tag name not equal to \'listok\'');
        }
        $this->number = mysql_real_escape_string($node->getAttribute('number'));
        if ($this->number === '') {
            throw new Exception('Missing listok attribute \'number\'');
        }
        $this->type = (int)($node->getAttribute('type'));
        if (!self::checkType($this->type)) {
            throw new Exception('Invalid listok type');
        }
        $this->description = mysql_real_escape_string($node->getAttribute('description'));
        $this->date = mysql_real_escape_string($node->getAttribute('date'));
        if (isset($class)) {
            $this->class = mysql_real_escape_string($class);
        } else {
            $this->class = 'NULL';
        }       
        
        // Инициализируем задачи
        $problemList = $node->getElementsByTagName('problem');
        $this->problemCount = $problemList->length;
        for ($i = 0; $i < $this->problemCount; $i++) {
            $this->problems[] = new TProblem($problemList->item($i), $i);
        }
    }
    
    function write2SQL() {
        global $db;
        $sql = 'INSERT INTO `PList` (`ListTypeID`, `ClassID`, `Number`, `Description`, `Date`) VALUES 
                (' . $this->type . ',
                 ' . $this->class . ',
                "' . $this->number . '",
                "' . $this->description . '",
                "' . $this->date . '")';
        if(!mysql_query($sql)) {
            throw new Exception('Could not insert listok into database: ' . mysql_error());
        }
        $ListID = mysql_insert_id();    // узнаём ID добавленной записи
        for ($i = 0; $i < $this->problemCount; $i++) {
            $this->problems[$i]->write2SQL($ListID);
        }
    }
    
    static function checkType($t) {
        global $db;
        if (!isset(self::$typesArray)) {
            $sql = 'SELECT `ID` FROM `PListType`';
            $result = mysql_query($sql);
            if(!$result) {
                throw new Exception('Selection error: ' . mysql_error());
            }
            while ($row = mysql_fetch_array($result)) {
                self::$typesArray[] = (int)$row['ID'];
            }
        }
        return in_array($t, self::$typesArray, true);
    }
}

class TPupil {
    public $name1;
    public $name2;
    public $name3;
    public $nick;
    
    function __construct(DOMElement $node, $internalNumber) {
        global $db;
        if ($node->tagName !== 'pupil'){
            throw new Exception('Tag name not equal to \'pupil\'');
        }
        $fullName = explode(' ', mysql_real_escape_string($node->textContent), 3);
        $this->name1 = isset($fullName[0])?$fullName[0]:'';
        $this->name2 = isset($fullName[1])?$fullName[1]:'';
        $this->name3 = isset($fullName[2])?$fullName[2]:'';
        $this->nick = mysql_real_escape_string($node->getAttribute('nick'));
    }
    
    function write2SQL($ClassID) {
        global $db;
        $sql = 'INSERT INTO `PPupil` (`ClassID`, `Name1`, `Name2`, `Name3`, `Nick`) VALUES 
                (' . $ClassID . ',
                "' . $this->name1 . '",
                "' . $this->name2 . '",
                "' . $this->name3 . '",
                "' . $this->nick . '")';
        if(!mysql_query($sql)) {
            throw new Exception('Could not insert pupil into database: ' . mysql_error());
        }
    }
}

class TClass {
    public $name;
    public $description;
    public $pupils;
    public $pupilCount;
    
    function __construct(DOMElement $node) {
        global $db;
        // Инициализируем сам класс
        if ($node->tagName !== 'class'){
            throw new Exception('Tag name not equal to \'class\'');
        }
        $this->name = mysql_real_escape_string($node->getAttribute('name'));
        if ($this->name === '') {
            throw new Exception('Missing class attribute \'name\'');
        }
        $this->description = mysql_real_escape_string($node->getAttribute('description'));
        
        // Инициализируем школьников
        $pupilList = $node->getElementsByTagName('pupil');
        $this->pupilCount = $pupilList->length;
        for ($i = 0; $i < $this->pupilCount; $i++) {
            $this->pupils[] = new TPupil($pupilList->item($i), $i);
        }
    }
    
    function write2SQL() {
        global $db;
        $sql = 'INSERT INTO `PClass` (`Name`, `Description`) VALUES 
                ("' . $this->name . '",
                 "' . $this->description . '")';
        if(!mysql_query($sql)) {
            throw new Exception('Could not insert class into database: ' . mysql_error());
        }
        $ClassID = mysql_insert_id();    // узнаём ID добавленной записи
        for ($i = 0; $i < $this->pupilCount; $i++) {
            $this->pupils[$i]->write2SQL($ClassID);
        }
        $Result['value'] = $ClassID;
        $Result['text'] = classDisplayName($this->name, $this->description);
        return $Result;
    }
}

function errorHandler($type, $message, $file, $line) {
    if (substr($message, 0, 23) === 'DOMDocument::loadXML():') {
        // ошибка парсинга XML
        throw new Exception('Invalid XML structure: ' . substr($message, 24));
    } else {
        // стандартный обработчик для AJAX
        ajaxErrorHandler($type, $message, $file, $line);
    }
}

function parseListok($xml, $class) {
    global $db;
    
    set_error_handler('errorHandler');

    $xml = str_replace("’", "'", $xml);
    $doc = new DOMDocument('1.0', 'utf8');
    $doc->loadXML($xml);
    $listok = new TListok($doc->documentElement, $class);
    
    $sql = 'START TRANSACTION';
    if(!mysql_query($sql)) {
        error_log('SQL error: ' . mysql_error());
        throw new Exception('SQL error');
    }
    
    try {
        $listok->write2SQL();
        $sql = 'COMMIT';
        if(!mysql_query($sql)) {
            throw new Exception('SQL error: ' . mysql_error());
        }
    } catch (Exception $e) {
        $sql = 'ROLLBACK';
        mysql_query($sql);
        error_log("Cannot upload to database. " . $e->getMessage());
        throw new Exception('SQL error');
    }
}

function parseClass($xml) {
    global $db;
    
    set_error_handler('errorHandler');

    $doc = new DOMDocument('1.0', 'utf8');
    $doc->loadXML($xml);
    
    $class = new TClass($doc->documentElement);
    
    $sql = 'START TRANSACTION';
    if(!mysql_query($sql)) {
        error_log('SQL error: ' . mysql_error());
        throw new Exception('SQL error');
    }
    
    try {
        $Result = $class->write2SQL();
        $sql = 'COMMIT';
        if(!mysql_query($sql)) {
            throw new Exception('SQL error: ' . mysql_error());
        }
    } catch (Exception $e) {
        $sql = 'ROLLBACK';
        mysql_query($sql);
        error_log("Cannot upload to database. " . $e->getMessage());
        throw new Exception('SQL error');
    }
    return $Result;
}

// Обрабатываем запрос
try {
    if ($_POST['type'] === 'listok') {
        parseListok($_POST['XML'], $_POST['Class']);
        $Response['code']    = 0;
        $Response['message'] = 'Listok uploaded successfully!';
    } elseif ($_POST['type'] === 'class') {
        $Response['result']  = parseClass($_POST['XML']);
        $Response['code']    = 0;
        $Response['message'] = 'Class uploaded successfully!';
    } else {
        throw new Exception('Incorrect choice');
    }
} catch (Exception $e) {
    $Response['code']    = 1;
    $Response['message'] = 'Upload process failed. ' . $e->getMessage().$sql;
}

// Возвращаем ответ
echo json_encode($Response);
?>