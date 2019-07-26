<?php

define('IN_CONDUIT', true);
define('AJAX', true);
require_once('/home/host1000218/shashkovs.ru/htdocs/www/vmsh_test/conduit/UserManagement.inc');
checkAccess(PUPIL_LEVEL);
require_once('AjaxError.inc');
require_once('FillSelectors.inc');

?>
<?php

// Защита от SQL-инъекции
$ClassID = (string)mysql_real_escape_string($_POST['Class']);
$ListID  = (string)mysql_real_escape_string($_POST['List']);

try {
    fillListSelector($ListID, $ClassID);
} catch (Exception $e) {
    triggerAjaxError(404);
}

?>