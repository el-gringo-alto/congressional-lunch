document.addEventListener('DOMContentLoaded', () => {

    // start the stream if it exists
    if (document.getElementById('stream') != null) {
        getTweetStream();
        // run every 10 seconds
        setInterval(getTweetStream, 20000);
    }

})

const parsedUrl = new URL(window.location.href);
var party = parsedUrl.searchParams.get('party');
const tweetId = parsedUrl.searchParams.get('id');

// initialize the currentTweets variable so we can use it for comparison later
var currentTweets;


function mkTweetFeed(tweets) {
    var htmlText = '';
    for (var item of tweets) {
        htmlText += buildTweet(item);
    }
    return htmlText;
}

function buildTweet(tweet, link=true) {
    var linkHtml = ''
    if (link) {
        linkHtml = `
            <div class="link-container">
                <a href="/tweet.php?id=${tweet.id}" aria-label="Go to single tweet page with id ${tweet.id}">
                    <span class="fas fa-angle-right"></span>
                </a>
            </div>`;
    }
    let tweetHtml = `
        <article class="tweet ${tweet.party.toLowerCase()}" aria-labelledby="${tweet.id}">
            <header class="tweet-header">
                <div class="profile-img">
                    <img src="/assets/imgs/thumbs/${tweet.handle}.jpg" alt="@${tweet.handle} twitter profile picture" width="48">
                </div>
                <div class="tweet-info">
                    <span class="name">${tweet.name}</span>
                    <span class="handle">@${tweet.handle}</span>
                </div>
                ${linkHtml}
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

    return tweetHtml;
}

function getTweetStream() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // only run if the response is different from what we already have
            if (this.responseText != currentTweets) {
                // make the html for the tweets and add it to the page
                document.getElementById('stream').innerHTML = mkTweetFeed(JSON.parse(this.responseText));
                // set the current json for the tweets
                // leave it as a string so we can use it later for comparison
                currentTweets = this.responseText;
            }
        }
    };

    if (party != null) {
        var queryParty = `party=${party}`;
    } else {
        var queryParty = ''
    }

    xmlhttp.open('GET', `/includes/stream.php?${queryParty}`, true);
    xmlhttp.send();
}
