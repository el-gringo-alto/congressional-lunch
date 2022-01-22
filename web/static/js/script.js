var source = new EventSource('/stream');
source.onmessage = function(event) {
    newTweet = buildTweet(JSON.parse(event.data))
    stream = document.getElementById('stream')
    stream.innerHTML = newTweet + stream.innerHTML;
};


function buildTweet(tweet, link=true) {
    return tweetHtml = `
        <article class="tweet ${tweet.party.toLowerCase()}" aria-labelledby="${tweet.id}">
            <header class="tweet-header">
                <div class="profile-img">
                    <img src="/static/imgs/thumbs/${tweet.handle}.jpg" alt="@${tweet.handle} twitter profile picture" width="48">
                </div>
                <div class="tweet-info">
                    <span class="name">${tweet.name}</span>
                    <span class="handle">@${tweet.handle}</span>
                </div>
                <div class="link-container">
                    <a href="/${tweet.id}" aria-label="Go to single tweet page with id ${tweet.id}">
                        <span class="fas fa-angle-right"></span>
                    </a>
                </div>
            </header>
            <div class="text" id="${tweet.id}">
                <p>${tweet.tweet}</p>
            </div>
            <time><span class="time">${tweet.time}</span>${tweet.date}</time>
            <footer class="tweet-footer">
                <span class="retweets"><span class="fas fa-retweet" aria-label="Number of retweets"></span>${tweet.retweets}</span>
                <span class="likes"><span class="far fa-heart" aria-label="Number of likes"></span>${tweet.likes}</span>
            </footer>
        </article>`;
}
