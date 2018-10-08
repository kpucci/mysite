function setup()
{
    loadStats();
    var id = document.getElementById("player-id").value;
    makeReq("GET", "/puckperfect/players/" + id, 200, populateProfile);
}

function populateProfile(responseText)
{
    console.log("-----Populating Player Profile-----");
    console.log(responseText);
    var player = JSON.parse(responseText);

    var first_name = player['first_name'];
    var last_name = player['last_name'];

    document.getElementById("player-name").innerHTML = first_name + " " + last_name;
    document.getElementById("player-name-2").innerHTML = first_name + " " + last_name;
}

function logout()
{

}

function goToLogin(responseText)
{
    window.location.href = "/";
}

function loadStats()
{
    document.getElementById("stats-link-2").classList.add("active");
    document.getElementById("drills-link-2").classList.remove("active");
    document.getElementById("stats").style.display = "block";
    document.getElementById("drills").style.display = "none";
}

function loadDrills()
{
    document.getElementById("drills-link-2").classList.add("active");
    document.getElementById("stats-link-2").classList.remove("active");
    document.getElementById("drills").style.display = "block";
    document.getElementById("stats").style.display = "none";

    var id = document.getElementById("player-id").value;
    makeReq("GET", "/puckperfect/playlists/" + id, 200, populateDrills);

}

function populateDrills(responseText)
{
    console.log("-----Repopulating drills-----");
    console.log(responseText);
  	var drills = JSON.parse(responseText);

    var carousel = document.getElementById("drill-carousel");
    var drill, item, card, cardDeck, cardBody, cardImg, cardTitle, cardText, cardBtn;

    // Remove old list of drills
    while(carousel.hasChildNodes()){
        carousel.removeChild(carousel.childNodes[0]);
    }

    var firstItem = true;
    var cardCount = 0;

    // Create new list of drills
    for(var i=(drills.length-1); i>=0; i--)
    {
        if(cardCount == 0)
        {
            item = document.createElement("div");
            item.classList.add("carousel-item");

            cardDeck = document.createElement("div");
            cardDeck.classList.add("card-deck");
        }
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

function practiceDrill(id)
{

}

function loadCatalog()
{
  var id = document.getElementById("player-id").value;
  makeReq("GET", "/puckperfect/catalog/" + id, 200, populateCatalog);
}

function populateCatalog(responseText)
{
  // TODO: Filter out drills that the player already has in their playlist
  console.log("-----Repopulating catalog-----");
  console.log(responseText);

}

function loadSettings()
{

}

function addToCatalog(id)
{
  var playerId = document.getElementById("player-id").value;

  var data = '{"player_id":"' + playerId + '", "drill_id": "' + id + '"}';

  makeReq("PUT", "/puckperfect/playlists/" + id, 201, populateDrills);
}

// setup load event
window.addEventListener("load", setup, true);
