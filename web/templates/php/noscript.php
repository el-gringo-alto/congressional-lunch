<noscript>
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
                <p>Javascript must be enabled in order to properly view this site.</p>
            </div>
            <time><span class="time"><?php echo date('h:i A'); ?></span><?php echo date('M j, Y'); ?></time>
            <footer class="tweet-footer">
                <span class="retweets"><span class="fas fa-retweet" aria-label="Retweets"></span><?php echo rand(0, 999); ?></span>
                <span class="likes"><span class="far fa-heart" aria-label="Likes"></span><?php echo rand(0, 999); ?></span>
            </footer>
        </article>
    </section>
</noscript>
