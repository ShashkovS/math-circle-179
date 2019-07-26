<?php
$REMOTE_ADDR          = htmlentities($_SERVER['REMOTE_ADDR'], ENT_QUOTES | ENT_IGNORE, "UTF-8");
$HTTP_X_FORWARDED_FOR = htmlentities($_SERVER['HTTP_X_FORWARDED_FOR'], ENT_QUOTES | ENT_IGNORE, "UTF-8");
$HTTP_CLIENT_IP       = htmlentities($_SERVER['HTTP_CLIENT_IP'], ENT_QUOTES | ENT_IGNORE, "UTF-8");
$HTTP_REFERER         = htmlentities($_SERVER['HTTP_REFERER'], ENT_QUOTES | ENT_IGNORE, "UTF-8");

try {
    $obj = json_decode(file_get_contents('php://input'));
} catch (Exception $e) {
    exit();
}


$time = new DateTime;
$txt = '<tr><td>'.$time->format(DateTime::ATOM).'</td>'
       .'<td>'.$REMOTE_ADDR.'</td>'
       .'<td>'.$HTTP_REFERER.'</td>'
       .'<td>'.$HTTP_X_FORWARDED_FOR.'</td>'
       .'<td>'.$HTTP_CLIENT_IP.'</td>'
       .'<td>'.$obj->key.'</td>'
       .'<td>'.$obj->name.'</td>'
       .'<td>'.$obj->ans.'</td>'
       .'</tr>';
$myfile = file_put_contents('karusel_stats.html', $txt.PHP_EOL , FILE_APPEND | LOCK_EX);

$Response['Ok?']         = 'Ok!';
echo json_encode($Response);
?>
