function setup()
{
    document.getElementById("player-type").checked = true;
    showPlayerInputs();
}

function showPlayerInputs()
{
    if(document.getElementById("player-type").checked == true)
    {
        document.getElementById("player-info-box").style.display = 'block';
        document.getElementById("parent-info-box").style.display = 'none';
        document.getElementById("info-header").innerHTML = "Player Info";
    }
}

function showCoachInputs()
{
    if(document.getElementById("coach-type").checked == true)
    {
        document.getElementById("player-info-box").style.display = 'none';
        document.getElementById("parent-info-box").style.display = 'none';
        document.getElementById("info-header").innerHTML = "Coach Info";
    }
}

function showParentInputs()
{
    if(document.getElementById("parent-type").checked == true)
    {
        document.getElementById("player-info-box").style.display = 'none';
        document.getElementById("parent-info-box").style.display = 'block';
        document.getElementById("info-header").innerHTML = "Parent Info";
    }
}

function register()
{
    var first_name = document.getElementById("first-name").value;
    var last_name = document.getElementById("last-name").value;
    var email = document.getElementById("email-input").value;
    var password = document.getElementById("password-input").value;

    // TODO: Check password confirmation

    if(document.getElementById("player-type").checked)
    {
        var hockey_level = document.getElementById("hockey-level").value;
        var skill_level = document.getElementById("skill-level").value;
        var hand = document.getElementById("left").checked;

        var data = '{"email":"' + email + '", "password": "' + password + '", "first_name":"' + first_name + '", "last_name": "' + last_name + '", "hockey_level": ' + hockey_level + ', "skill_level": ' + skill_level + ', "hand": ' + hand + '}';
        makeReq("POST", "/puckperfect/players", 201, goToLogin, data);
    }
    else if(document.getElementById("coach-type").checked)
    {
        var data = '{"email":"' + email + '", "password": "' + password + '", "first_name":"' + first_name + '", "last_name": "' + last_name + '"}';
        makeReq("POST", "/puckperfect/coaches", 201, goToLogin, data);
    }
    else
    {
        var child_name = document.getElementById("child-search").value;
        var data = '{"email":"' + email + '", "password": "' + password + '", "first_name":"' + first_name + '", "last_name": "' + last_name + '", "child_name": "' + child_name + '"}';
        makeReq("POST", "/puckperfect/parents", 201, goToLogin, data);
    }

}

function goToLogin(responseText)
{
    window.location.href = "/puckperfect/";
}

// setup load event
window.addEventListener("load", setup, true);
