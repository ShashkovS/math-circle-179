<?php

if (!defined('IN_CONDUIT')){
    // Попытка прямого доступа к файлу
    exit();
}

?>
<?php

// Возвращаем html заголовок, соответствующий ошибке
function triggerAjaxError($err) {
    switch ($err) {
        case 404: header('HTTP/1.0 404 Not Found');
        case 504: header('HTTP/1.0 504 Gateway Timeout');
        case 500:
        default : header('HTTP/1.0 500 Internal Server Error');
    }
    exit();
}

function ajaxErrorHandler($number, $string, $file, $line) {
    error_log($string . ' in ' . $file . ' on line ' . $line);
    triggerAjaxError(500);
}

set_error_handler('ajaxErrorHandler');

?>