/**
 * Setup the webpage
 */
function setup()
{
    loadStats();
    var id = document.getElementById("player-id").value;
    var token = localStorage.getItem("access_token");
    makeTokenReq("GET", "/players/" + id, 200, populateProfile, null, token);
}

/**
 * Callback
 * Populate the profile with the player's information
 * @param {String} responseText - HTTP response text
 */
function populateProfile(responseText)
{
    // Print response text to console for debugging
    console.log("-----Populating Player Profile-----");
    console.log(responseText);

    // Parse the text into JSON
    var player = JSON.parse(responseText);

    // Get the player's name from the response
    var first_name = player['first_name'];
    var last_name = player['last_name'];

    // Display the player's name
    document.getElementById("player-name").innerHTML = first_name + " " + last_name;
    document.getElementById("player-name-2").innerHTML = first_name + " " + last_name;
}

function logout()
{

}

/**
 * Go to the login page
 * @param  {String} responseText - HTTP response text
 */
function goToLogin(responseText)
{
    window.location.href = "/";
}

/**
 * Load the stats view
 */
function loadStats()
{
    // Change stats link to active
    document.getElementById("stats-link-2").classList.add("active");

    // Change drills link to inactive
    document.getElementById("drills-link-2").classList.remove("active");

    // Show stats view
    document.getElementById("stats").style.display = "block";

    // Hide drills view
    document.getElementById("drills").style.display = "none";
}

/**
 * Load the drills view
 */
function loadDrills()
{
    // Change drills link to active
    document.getElementById("drills-link-2").classList.add("active");

    // Change stats link to inactive
    document.getElementById("stats-link-2").classList.remove("active");

    // Show drills view
    document.getElementById("drills").style.display = "block";

    // Hide stats view
    document.getElementById("stats").style.display = "none";

    // Get the player's playlist of drills
    var id = document.getElementById("player-id").value;
    makeReq("GET", "/playlists/" + id, 200, populateDrills);
}

/**
 * Callback
 * Populate the drills view with the player's playlist
 * @param  {String} responseText - HTTP response text
 */
function populateDrills(responseText)
{
    // Print response text to console for debugging
    console.log("-----Repopulating drills-----");
    console.log(responseText);

    // Parse the text to JSON
  	var drills = JSON.parse(responseText);

    // Create variables
    var carousel = document.getElementById("drill-carousel");
    var drill, item, card, cardDeck, cardBody, cardImg, cardTitle, cardText, cardBtn;
    var firstItem = true;
    var cardCount = 0;

    // Remove old list of drills
    while(carousel.hasChildNodes()){
        carousel.removeChild(carousel.childNodes[0]);
    }

    // Create new list of drills
    for(var i=(drills.length-1); i>=0; i--)
    {
        // If first card in deck, add new deck to carousel
        if(cardCount == 0)
        {
            item = document.createElement("div");
            item.classList.add("carousel-item");

            cardDeck = document.createElement("div");
            cardDeck.classList.add("card-deck");
        }

        // Make first item active
        if(firstItem)
        {
            item.classList.add("active");
            firstItem = false;
        }

        // Create card for drill
        card = document.createElement("div");
        card.classList.add("card");

        // Create card image
        cardImg = document.createElement("img");
        cardImg.classList.add("card-img-top");
        cardImg.src = "../static/css/generic_drill_background.jpg";
        cardImg.alt = "Drill background";

        // Create card body
        cardBody = document.createElement("div");
        cardBody.classList.add("card-body");

        // Create card title
        cardTitle = document.createElement("h5");
        cardTitle.classList.add("card-title");
        cardTitle.innerHTML = drills[i]['name'];

        // Create card text
        cardText = document.createElement("p");
        cardText.classList.add("card-text");
        cardText.innerHTML = drills[i]['description'];

        // Create card button
        cardBtn = document.createElement("button");
        cardBtn.classList.add("btn");
        cardBtn.classList.add("btn-sm");
        cardBtn.classList.add("btn-secondary");
        cardBtn.type = "button";
        cardBtn.onclick = "practiceDrill(" + drills[i]['id'] + ");";
        cardBtn.innerHTML = "Practice";

        // Add title, text, and button to body
        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardText);

        // Add image and body to card
        card.appendChild(cardImg);
        card.appendChild(cardBody);
        card.appendChild(cardBtn);

        // Add card to card deck
        cardDeck.appendChild(card);

        cardCount++;

        // Three cards per deck
        if(cardCount == 3 || i == 0)
        {
            // Add card deck to carousel item
            item.appendChild(cardDeck);

            // Add item to carousel
            carousel.appendChild(item);

            // Reset count
            cardCount = 0;
        }
	  }
}

/**
 * Create practice run for drill
 * @param  {int} id - the id of the drill being practiced
 */
function practiceDrill(id)
{

}

/**
 * Load full catalog of drills
 */
function loadCatalog()
{
  var id = document.getElementById("player-id").value;
  makeReq("GET", "/catalog/" + id, 200, populateCatalog);
}

/**
 * Callback
 * Populate catalog view with drills
 * @param  {String} responseText - HTTP response text
 */
function populateCatalog(responseText)
{
  // TODO: Filter out drills that the player already has in their playlist
  console.log("-----Repopulating catalog-----");
  console.log(responseText);

}

/**
 * Load account settings
 */
function loadSettings()
{

}

/**
 * Add a drill to the player's playlist
 * @param {int} id - the id of the drill to add
 */
function addToPlaylist(id)
{
  var playerId = document.getElementById("player-id").value;

  var data = '{"player_id":"' + playerId + '", "drill_id": "' + id + '"}';

  makeReq("PUT", "/playlists/" + id, 201, populateDrills);
}

// setup load event
window.addEventListener("load", setup, true);
