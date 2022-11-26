function load_everything() {
    // display only news section when first loaded
    document.getElementById("search").style.display = 'none';

    // define news/search tabs onclick behavior
    let tabs = document.getElementsByClassName("tab");
    for (let tab of tabs) {
        tab.onclick = function () {
            show_news_or_search(tab.id);
        }
    }

    // load headlines slideshows, word cloud, CNN & Fox News
    load_generic_headlines();
    load_word_cloud_words();
    load_cnn_fox_headlines();

    // set default dates of the date selectors
    set_default_date();

    // load initial sources when category=all
    load_sources("all");

    // define category drop-down menu onclick behavior
    let category = document.getElementById("category");
    category.onchange = function () {
        load_sources(category.options[category.selectedIndex].value);
    };

    // define submit onclick behavior
    document.getElementById("search-button").onclick = function (event) {
        event.preventDefault(); // prevent the page from refreshing

        // only submit the form when all fields have valid inputs
        if (document.getElementById("search-form").reportValidity()) {
            load_search_results();
        }
    };

    // define reset onlick behavior
    document.getElementById("clear-button").onclick = reset_form;
}

function load_generic_headlines() {
    fetch("/generic/")
        .then(
            function(response) {
                if (response.status !== 200) {
                    console.log(response);
                    return;
                }

                response.json()
                    .then(data => {
                        display_generic_headlines(data.articles);
                    });
            }
        )
        .catch(err => {
            console.log(err);
        })
}

function load_cnn_fox_headlines() {
    fetch("/cnn-fox/")
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.log(response);
                    return;
                }

                response.json()
                    .then(data => {
                        display_cnn_fox_headlines(data.articles);
                    });

            }
        )
        .catch(err => {
            console.log(err);
        });
}

function load_word_cloud_words() {
    fetch("/word-cloud/")
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.log(response);
                    return;
                }

                response.json()
                    .then(data => {
                        display_word_cloud(data.words);
                    });
            }
        )
        .catch(err => {
            console.log(err);
        })
}

function load_sources(value) {
    fetch(`/get-sources/${value}`)
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.log(response);
                    return;
                }

                response.json()
                    .then(data => {
                        display_sources(data);
                    });

            }
        )
        .catch(err => {
            console.log(err);
        })
}

function load_search_results() {
    let keyword = document.getElementById("keyword").value,
        from_date = document.getElementById("from-date").value,
        to_date = document.getElementById("to-date").value,
        category = document.getElementById("category").value,
        source = document.getElementById("source").value;

    // check date range is valid
    let start_date = new Date(from_date), finish_date = new Date(to_date);
    if (finish_date < start_date) {
        alert("Incorrect time.");
        return;
    }

    fetch(`/search/?kw=${keyword}&from=${from_date}&to=${to_date}&cat=${category}&src=${source}`)
        .then(
            function(response) {
                if (response.status !== 200) {
                    console.log(response);
                    return;
                }

                response.json()
                    .then(data => {
                        display_search_results(data);
                    });
            }
        )
        .catch(err => {
            console.log(err);
        })
}

function display_generic_headlines(jsonObj) {
    let slides = document.getElementsByClassName("generic-headline");
    let text_title = document.getElementsByClassName("gh-title");
    let text_desc = document.getElementsByClassName("gh-desc");
    for (let i = 0; i < slides.length; i++) { // hide everything at the beginning
        slides[i].style.display = "none";
    }
    slide_index ++;
    // reset slide_index (start the slideshow over)
    if (slide_index === slides.length) {slide_index = 1}

    // link entire div to news
    let slide = document.getElementById("top-col-news").firstElementChild;
    slide.href = jsonObj[slide_index-1].url;

    // set image, title, description
    slides[slide_index-1].getElementsByTagName("img")[0].src =
        jsonObj[slide_index-1].urlToImage;
    text_title[slide_index-1].textContent = jsonObj[slide_index-1].title;
    text_desc[slide_index-1].textContent = jsonObj[slide_index-1].description;
    slides[slide_index-1].style.display = "block";
    setTimeout(function() {display_generic_headlines(jsonObj)}, 4000);
}

function display_cnn_fox_headlines(jsonObj) {
    let hl_div = document.getElementsByClassName("hl-link");
    let hl_articles = document.getElementsByClassName("hl-text-container");

    for (let i=0; i<hl_articles.length; i++) {
        // link entire div to the news
        hl_div[i].href = jsonObj[i].url;

        // populate card with image, title, description
        let hl_article = hl_articles[i];
        hl_article.getElementsByTagName("img")[0].src = jsonObj[i].urlToImage;
        hl_article.getElementsByClassName("hl-title")[0].textContent = jsonObj[i].title;
        hl_article.getElementsByTagName("p")[0].textContent = jsonObj[i].description;
    }
}

function display_word_cloud(jsonObj){
    // set the dimensions and margins of the graph
    let width = 320, height = 250;

    // append the svg object to the body of the page
    let svg = d3.select("#word_cloud_container")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // Constructs a new cloud layout instance.
    // It run an algorithm to find the position of words that suits your requirements
    let layout = d3.layout.cloud()
        .size([width, height])
        .words(jsonObj.map(function(d) { return {text: d.word, size:d.size}; }))
        .padding(10) //space between words
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .fontSize(function(d) { return d.size;}) // font size of words
        .on("end", draw);
    layout.start();

    // This function takes the output of 'layout' above and draw the words
    function draw(words) {
        svg.append("g")
            .attr("transform",
                "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter()
            .append("text")
            .style("font-size", function(d) { return d.size + "px";})
            .style("fill", "#000000")
            .attr("text-anchor", "middle")
            .style("font-family", "Impact")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
    }
}

function display_sources(jsonObj) {
    let source_drop_down = document.getElementById("source");
    // remove all options
    for (let i = source_drop_down.length - 1; i > 0; i--) {
        source_drop_down.remove(i);
    }
    // add new sources for the category
    for (let i = 0; i < jsonObj.source_names.length; i++) {
    //for (let source of jsonObj.sources_names){
        let option = document.createElement("option");
        option.text = jsonObj.source_names[i];
        option.value = jsonObj.source_ids[i];
        source_drop_down.add(option);
    }
}

function clear_search_results(show_less_div, show_more_div, results_div) {
    // clear last-time search results
    while (show_less_div.firstChild) {
        show_less_div.firstChild.remove();
    }
    while (show_more_div.firstChild) {
        show_more_div.firstChild.remove();
    }
    if (results_div.childElementCount > 2) {
        results_div.removeChild(results_div.children[2]);
    }
}

function display_search_results(jsonObj) {
    let results_div = document.getElementById("search-results"),
        show_less_div = results_div.children[0],
        show_more_div = results_div.children[1];
    clear_search_results(show_less_div, show_more_div, results_div);

    // hide articles in show-more by default
    show_more_div.style.display = "none";

    // check error
    if (jsonObj.status === "error") {
        alert(jsonObj.message);
        return;
    }

    let articles = jsonObj.articles;

    // if no article returned
    if (articles.length === 0) {
        let no_results = document.createElement("p");
        no_results.classList.add("no-results");
        no_results.appendChild(document.createTextNode("No results"));
        results_div.appendChild(no_results);
        return;
    }

    // create card display for each article
    for (let i = 0; i < articles.length; i++) {
        let result_card = create_result_card(articles[i]);
        let result_card_expanded = create_result_card_expanded(articles[i]);
        // define result card onclick behavior
        result_card.onclick = function () {
            result_card.style.display = "none";
            result_card_expanded.style.display = "grid";
        };

        // add close button
        let close_sign = document.createElement("a");
        close_sign.href = "#";
        close_sign.classList.add("close-sign");
        close_sign.textContent = "x";
        // define close button onclick behavior
        close_sign.onclick = function () {
            result_card.style.display = "grid";
            result_card_expanded.style.display = "none";
        };
        result_card_expanded.appendChild(close_sign);

        // put first 5 articles in show-less div, and the rest in show-more div
        if (i < 5) {
            show_less_div.appendChild(result_card);
            show_less_div.appendChild(result_card_expanded);
        }
        else {
            show_more_div.appendChild(result_card);
            show_more_div.appendChild(result_card_expanded);
        }
    }

    if (articles.length > 5) {
        // implement show-more show-less
        let show_more_less = document.createElement("button");
        show_more_less.id = "show-more-less-button";
        show_more_less.classList.add("show-more");
        show_more_less.textContent = "Show More";
        results_div.appendChild(show_more_less);

        show_more_less.onclick = function () {
            if (show_more_less.className === "show-more") {
                show_more_div.style.display = "block";
                show_more_less.classList.remove("show-more");
                show_more_less.classList.add("show-less");
                show_more_less.textContent = "Show Less";
            } else {
                show_more_div.style.display = "none";
                show_more_less.classList.remove("show-less");
                show_more_less.classList.add("show-more");
                show_more_less.textContent = "Show More";
            }
        }
    }
}

function create_result_card_expanded(article) {
    let result_card = create_result_card(article);
    result_card.classList.add("expanded");
    result_card.style.display = "none";

    /* change to detailed information */
    let text_div = result_card.getElementsByClassName("result-text-div")[0];
    // remove one line description
    text_div.removeChild(text_div.childNodes[1]);

    // add author info
    let author_p = document.createElement("p");
    author_p.innerHTML = `<b>Author:</b>  ${article.author}`;
    text_div.appendChild(author_p);

    // add source info
    let source_p = document.createElement("p");
    source_p.innerHTML = `<b>Source:</b>  ${article.source.name}`;
    text_div.appendChild(source_p);

    // add date info
    let date_p = document.createElement("p");
    let date = new Date(article.publishedAt);
    date = `${("0" + (date.getMonth() + 1)).slice(-2)}/${("0" + date.getDate()).slice(-2)}/${date.getFullYear()}`;
    date_p.innerHTML = `<b>Date:</b>  ${date}`;
    text_div.appendChild(date_p);

    // add detailed description
    let desc_p = document.createElement("p");
    desc_p.classList.add("desc-p");
    desc_p.textContent = article.description;
    text_div.appendChild(desc_p);

    // add link to original news post
    let link_to_news = document.createElement("a");
    link_to_news.href = article.url;
    link_to_news.target = "_blank";
    link_to_news.textContent = "See Original Post";
    text_div.appendChild(link_to_news);

    return result_card;
}

function create_result_card(article) {
    let result_card = document.createElement("div");
    result_card.classList.add("result-card");

    // create img div for result card
    let result_img_div = document.createElement("div");
    result_img_div.classList.add("result-img-div");

    let result_img = document.createElement("img");
    result_img.src = article.urlToImage;

    result_img_div.appendChild(result_img);
    result_card.appendChild(result_img_div);

    // create text div for result card
    let result_text_div = document.createElement("div");
    result_text_div.classList.add("result-text-div");

    let result_title = document.createElement("h3");
    result_title.textContent = article.title;
    let result_desc = document.createElement("p");
    let desc = article.description.slice(0, 70);
    // remove html tags from returned description
    desc = desc.replace(/(<\w+>)+/, "");
    // display only one line with ellipsis cut off
    desc = desc.replace(/\W*\w+\W*$/, "...");
    result_desc.textContent = desc;

    result_text_div.appendChild(result_title);
    result_text_div.appendChild(result_desc);

    // put img and text in result cards
    result_card.appendChild(result_img_div);
    result_card.appendChild(result_text_div);

    return result_card;
}

function show_news_or_search(clicked_tab_id) {
    let news_div = document.getElementById("news");
    let search_div = document.getElementById("search");

    let tab_news = document.getElementById("tab-news");
    let tab_search = document.getElementById("tab-search");

    if (tab_news.classList.contains("active") && clicked_tab_id === "tab-search") {
        tab_news.classList.remove("active");
        tab_search.classList.add("active");
        search_div.style.display = "flex";
        news_div.style.display = "none";
    }
    else if (tab_search.classList.contains("active") && clicked_tab_id === "tab-news") {
        tab_news.classList.add("active");
        tab_search.classList.remove("active");
        news_div.style.display = "flex";
        search_div.style.display = "none";
    }
}

function set_default_date() {
    let curr_day = new Date();
    let week_ago = new Date();
    week_ago.setDate(curr_day.getDate() - 7);
    document.getElementById("from-date").valueAsDate = week_ago;
    document.getElementById("to-date").valueAsDate = curr_day;
}

function reset_form() {
    // reset the form
    document.getElementById("search-form").reset();
    // set default dates
    set_default_date();
    // clears previous search results
    let results_div = document.getElementById("search-results"),
        show_less_div = results_div.children[0],
        show_more_div = results_div.children[1];
    clear_search_results(show_less_div, show_more_div, results_div);
}

window.onload = load_everything;
var slide_index = 0;