document.addEventListener('DOMContentLoaded', () => {

    // Only run this code on pages that display the feed
    let stream = document.getElementById('stream');
    if (stream) {
        // Figure out the query party so it can be used in urls
        const parsedUrl = new URL(window.location.href);
        const party = parsedUrl.searchParams.get('party');
        let queryParty;

        if (party != null) {
            queryParty = `party=${party}`;
        } else {
            queryParty = '';
        }


        // Server send event to get newly created tweet and adds it to the top of the feed
        const source = new EventSource(`/stream?${queryParty}`);
        source.onmessage = (event) => {
            let newTweet = buildTweet(JSON.parse(event.data));
            stream.innerHTML = newTweet + stream.innerHTML;
        };

        source.onerror = (err) => {
          console.error('EventSource failed:', err);
        };


        // Fetch more tweets and add the the bottom of the feed when scroll reaches bottom
        window.onscroll = () => {
            if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {

                const addStream = (lastId) => {
                    let xmlhttp = new XMLHttpRequest();
                    xmlhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            resp = JSON.parse(this.responseText)

                            for (tweet of resp) {
                                // Build the tweets and add them to the bottom of the feed
                                if (typeof document.getElementById(tweet.id) !== 'undefined') {
                                    let newTweet = buildTweet(tweet);
                                    stream.innerHTML += newTweet;
                                }
                            }
                        }
                    };

                    xmlhttp.open('GET', `/stream-cont?id=${lastId}&${queryParty}`, true);
                    xmlhttp.send();
                }

                addStream(stream.lastElementChild.id);
            }
        };
    }
});



const buildTweet = (tweet) => {
    return tweetHtml = `
        <article class="tweet ${tweet.party}" aria-label="${tweet.name} tweet with id ${tweet.id}" aria-describedby="description-${tweet.id}" id="${tweet.id}">
            <header class="tweet-header">
                <div class="profile-img">
                    <img src="/static/imgs/thumbs/${tweet.handle}.jpg" alt="@${tweet.handle} twitter profile picture" width="48" loading="lazy">
                </div>
                <div class="tweet-info">
                    <span class="name">${tweet.name}</span>
                    <span class="handle">@${tweet.handle}</span>
                </div>
                <div class="link-container">
                    <a href="/tweet/${tweet.id}" aria-label="Go to single tweet page with id ${tweet.id}">
                        <span class="fas fa-angle-right"></span>
                    </a>
                </div>
            </header>
            <div class="text" id="description-${tweet.id}">
                <p>${tweet.tweet}</p>
            </div>
            <time><span class="time">${tweet.time}</span>${tweet.date}</time>
            <footer class="tweet-footer">
                <span class="retweets"><span class="fas fa-retweet" aria-label="Number of retweets"></span>${tweet.retweets}</span>
                <span class="likes"><span class="far fa-heart" aria-label="Number of likes"></span>${tweet.likes}</span>
            </footer>
        </article>`;
}
