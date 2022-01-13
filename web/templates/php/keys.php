<?php
    $production = true;
    if ($production == true) {
        $key_path = '/home/sam/congressional-lunch/keys.ini';
    } else {
        $key_path = $_SERVER['DOCUMENT_ROOT'] . '/../../keys_dev.ini';
    }
    $keys = parse_ini_file($key_path, true)['database'];
?>
