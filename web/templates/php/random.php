<?php
    $keys = json_decode(file_get_contents('/home/sam/congressional-lunch/keys/db_keys.json'));
    try {
        $conn = new PDO('mysql:host=localhost;dbname=congressional_lunch', $keys->user, $keys->password);

        $query = $conn->prepare('SELECT id FROM tweets ORDER BY RAND() LIMIT 1');

        $query->execute();
        $tweet = $query->fetch(PDO::FETCH_ASSOC);

        header('Location: /tweet.php?id=' . $tweet['id']);
        die();

    } catch(PDOException $e) {
        echo 'Connection failed: ' . $e->getMessage();
    }
 ?>
