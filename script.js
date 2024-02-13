document.addEventListener("DOMContentLoaded", function() {
    const headlineContainer = document.getElementById("headline-container");

    // Get headlines from the JSON file
    fetch('ArticleHeadlines.json')
        .then(response => response.json())
        .then(data => {
            // Display headlines on the webpage
            data.forEach(article => {
                const headlineBox = document.createElement("div");
                headlineBox.classList.add("headline-box"); // Add the box class

                // insert HTML content to the div
                headlineBox.innerHTML = `<a href="${article.link}" target="_blank">
                <b>${article.title}</b></a>
                <br>
                <i>${article.pub_date}</i>`;
                
                // insert the div to the headline container
                headlineContainer.appendChild(headlineBox);
            });
        })
        .catch(error => console.error('Error fetching headlines:', error));
});