<?php
    $title = 'About';
    include $_SERVER['DOCUMENT_ROOT'] . '/../templates/header.php';
?>

<section class="single-tweet">
    <article class="tweet" aria-labelledby="name" aria-describedby="description">
        <header class="tweet-header">
            <div class="profile-img">
                <img src="assets/imgs/samschultheis.jpg" alt="Personal image" width="48">
            </div>
            <div class="tweet-info">
                <span class="name" id="name">Sam Schultheis</span>
                <span class="handle" style="text-decoration: line-through;">@Sam_Schultheis</span>
            </div>
        </header>
        <div class="text" id="description">
            <p>Tweets generated through machine learning using tweets from a congressman&apos;s own party.</p>
            <p>These tweets are <strong>fake</strong> and do <strong>not</strong> represent the views nor beliefs of the person they are credited to.</p>
            <p><a href="http://samschultheis.com">#PersonalWebsite</a></p>
        </div>
        <time><span class="time"><?php echo date('h:i A'); ?></span><?php echo date('M j, Y'); ?></time>
        <footer class="tweet-footer">
            <span class="retweets"><span class="fas fa-retweet" aria-label="Retweets"></span><?php echo rand(0, 999); ?></span>
            <span class="likes"><span class="far fa-heart" aria-label="Likes"></span><?php echo rand(0, 999); ?></span>
        </footer>
    </article>

</section>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/../templates/footer.php'; ?>
