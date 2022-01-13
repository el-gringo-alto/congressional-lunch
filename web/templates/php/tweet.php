<?php
    $keys = json_decode(file_get_contents('/home/sam/congressional-lunch/keys/db_keys.json'));
    try {
        $id = $_GET['id'];
        if (ctype_digit($id) || $id == null) {
            $conn = new PDO('mysql:host=localhost;dbname=congressional_lunch', $keys->user, $keys->password);

            if ($id == null) {
                $query = $conn->prepare('SELECT * FROM tweets ORDER BY RAND() LIMIT 1');
            } else {
                $query = $conn->prepare('SELECT * FROM tweets WHERE id=:value LIMIT 1');
                $query->bindParam(':value', $id);
            }

            $query->execute();
            $tweet = $query->fetch(PDO::FETCH_ASSOC);
        } else {
            http_response_code(404);
            include $_SERVER['DOCUMENT_ROOT'] . '/error/404.php';
            die();
        }
    } catch(PDOException $e) {
        echo 'Connection failed: ' . $e->getMessage();
    }

    $title = "Single Tweet";
    $description = "@$tweet[handle]: $tweet[tweet]";
    include $_SERVER['DOCUMENT_ROOT'] . '/../templates/header.php';
?>

<section class="single-tweet">
    <article class="tweet <?=strtolower($tweet['party'])?>" aria-labelledby="<?=$tweet['id']?>">
        <header class="tweet-header">
            <div class="profile-img">
                <img src="/assets/imgs/thumbs/<?=$tweet['handle']?>.jpg" alt="@<?=$tweet['handle']?> twitter profile picture" width="48">
            </div>
            <div class="tweet-info">
                <span class="name"><?=$tweet['name']?></span>
                <span class="handle">@<?=$tweet['handle']?></span>
            </div>
        </header>
        <div class="text" id="<?=$tweet['id']?>">
            <p><?=$tweet['tweet']?></p>
        </div>
        <time><span class="time"><?=$tweet['time']?></span><?=$tweet['date']?></time>
        <footer class="tweet-footer">
            <span class="retweets"><span class="fas fa-retweet" aria-label="Number of retweets"></span><?=$tweet['retweets']?></span>
            <span class="likes"><span class="far fa-heart" aria-label="Number of likes"></span><?=$tweet['likes']?></span>
        </footer>
    </article>
</section>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/../templates/footer.php'; ?>
