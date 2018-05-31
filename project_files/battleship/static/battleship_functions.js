// THIS CODE IS A DISASTER TO READ THROUGH.. I AM SO SORRY!

// A:a3-a7;b:b3-b6;s:c3-c5
// A:b3-b7;b:c3-c6;s:d3-d5

var name1;
var name2;
var ships1;
var ships2;
var aircraft1;
var aircraft2;
var battleship1;
var battleship2;
var submarine1;
var submarine2;
var currentPlayer = 1;
var lockedIn = null;
var missedHits1 = [];
var missedHits2 = [];
var bombedHits1 = [];
var bombedHits2 = [];
var player1Score = 0;
var player2Score = 0;

function Aircraft(spaces)
{
  this.space1 = new Object();
  this.space2 = new Object();
  this.space3 = new Object();
  this.space4 = new Object();
  this.space5 = new Object();

  this.space1.name = spaces[0];
  this.space1.status = "safe";

  this.space2.name = spaces[1];
  this.space2.status = "safe";

  this.space3.name = spaces[2];
  this.space3.status = "safe";

  this.space4.name = spaces[3];
  this.space4.status = "safe";

  this.space5.name = spaces[4];
  this.space5.status = "safe";
  
  this.shipStatus = "afloat";
  
  this.shipLength = 5;
}

function Battleship(spaces)
{
  this.space1 = new Object();
  this.space2 = new Object();
  this.space3 = new Object();
  this.space4 = new Object();

  this.space1.name = spaces[0];
  this.space1.status = "safe";

  this.space2.name = spaces[1];
  this.space2.status = "safe";

  this.space3.name = spaces[2];
  this.space3.status = "safe";

  this.space4.name = spaces[3];
  this.space4.status = "safe";
  
  this.shipStatus = "afloat";
  
  this.shipLength = 4;
}

function Submarine(spaces)
{
  this.space1 = new Object();
  this.space2 = new Object();
  this.space3 = new Object();

  this.space1.name = spaces[0];
  this.space1.status = "safe";

  this.space2.name = spaces[1];
  this.space2.status = "safe";

  this.space3.name = spaces[2];
  this.space3.status = "safe";
  
  this.shipStatus = "afloat";
  
  this.shipLength = 3;
}


function OpenPlayerInfo()
{
  document.getElementById('player').style.display='block';
}

function CancelButton(modalName)
{
  document.getElementById(modalName).style.display='none';
}

function StartButton()
{
  // alert("Current Player: " + currentPlayer);
  document.getElementById('startpage').style.display='none';
  if(currentPlayer == 1)
  {
    SetAircraft(aircraft1);
    SetBattleship(battleship1);
    SetSubmarine(submarine1);
    SetMissed();
    SetBombed();
  }
  else if(currentPlayer == 2)
  {
    SetAircraft(aircraft2);
    SetBattleship(battleship2);
    SetSubmarine(submarine2);
    SetMissed();
    SetBombed();
  }

}

function SubmitButton()
{ 
    
  var playerLabel = document.getElementById('player-nlabel').textContent.split(" ");
  // PLAYER 1 ------------------------------------------------------------------
  if(playerLabel[1] == "1")
  {
    name1 = document.getElementById('player-ninput').value;
    ships1 = document.getElementById('player-sinput').value;
    document.getElementById('player1-name').innerHTML = name1;
    if(name1 == "")
    {
      alert("You need to enter a name!");
      return;
    }
    else if(ships1 == "")
    {
      alert("You need to enter your game pieces!");
      return;
    }
    else
    {
      // Get game pieces for player 1
      var ships1_split = ships1.split(";");
      var ships1_array = GetGamePieces(ships1_split);
      if(ships1_array != null)
      {
        aircraft1 = ships1_array[0];
        battleship1 = ships1_array[1];
        submarine1 = ships1_array[2];
        // Reset labels and input boxes for player 2
        document.getElementById('player-ninput').value = null;
        document.getElementById('player-sinput').value = null;
        document.getElementById('player-nlabel').innerHTML='Player 2';
      }
    }
  }
  // PLAYER 2 ------------------------------------------------------------------
  else
  {
    name2 = document.getElementById('player-ninput').value;
    ships2 = document.getElementById('player-sinput').value;
    document.getElementById('player2-name').innerHTML = name2;
    if(name2 == null)
    {
      alert("You need to enter a name!");
      return;
    }
    else if(ships2 == null)
    {
      alert("You need to enter your battleships!");
      return;
    }
    else
    {
      // Get game pieces for player 2
      var ships2_split = ships2.split(";");
      var ships2_array = GetGamePieces(ships2_split);

      if(ships2_array != null)
      {
        aircraft2 = ships2_array[0];
        battleship2 = ships2_array[1];
        submarine2 = ships2_array[2];
        document.getElementById('player').style.display='none';
        document.getElementById('startpage').style.display='block';
        document.getElementById('start-label').innerHTML = name1 + ", it's your turn!";
      }
    }
  }

}

function ClearGameBoard(TorB)
{
  var row;
  var col;
  var colCode = 64;
  var tableID = TorB + "_";
  var cellID;
  for(col=1;col<11;col++)
  {
    colCode++;
    for(row=1;row<11;row++)
    {
      cellID = tableID + String.fromCharCode(colCode) + row;
      document.getElementById(cellID).style.backgroundColor = "#bfefff";
      document.getElementById(cellID).innerHTML = null;
    }
    // alert(cellID);
  }
}


function GetGamePieces(ships)
{
  var aircraft;
  var aircraftSpaces;
  var battleship;
  var battleshipSpaces;
  var submarine;
  var submarineSpaces;
  var ship_trim;
  var spaces;
  var aircraftRegEx = /^a(:|:\(|\()((([a-j])([1-6])\-\4([5-9]|10))|(([a-f])([1-9]|10)\-([e-j])\9))/i;
  var battleshipRegEx = /^b(:|:\(|\()((([a-j])([1-7])\-\4([4-9]|10))|(([a-g])([1-9]|10)\-([d-j])\9))/i;
  var submarineRegEx = /^s(:|:\(|\()((([a-j])([1-8])\-\4([3-9]|10))|(([a-h])([1-9]|10)\-([c-j])\9))/i;
  // var spaceRegEx = /[a-j]\d0?\-[a-j]\d0?/gi;
  // alert(ships.length);
  for(i = 0; i<ships.length; i++)
  {
    ship_trim = ships[i].trim();
    // alert("i: " + i);
    // Use regular expression to search for different ships
    // alert(ship_trim);
    if(aircraftRegEx.test(ship_trim))
    {
      aircraftSpaceEnds = ship_trim.match(aircraftRegEx)[2].split("-");
      aircraftSpaces = GetAircraftSpaces(aircraftSpaceEnds);
      aircraft = new Aircraft(aircraftSpaces);
      // alert("Aircraft Spaces: " + aircraftSpaces);
    }
    else if(battleshipRegEx.test(ship_trim))
    {
      battleshipSpaceEnds = ship_trim.match(battleshipRegEx)[2].split("-");
      battleshipSpaces = GetBattleshipSpaces(battleshipSpaceEnds);
      battleship = new Battleship(battleshipSpaces);
      // alert("Battleship Spaces: " + battleshipSpaces);
    }
    else if(submarineRegEx.test(ship_trim))
    {
      submarineSpaceEnds = ship_trim.match(submarineRegEx)[2].split("-");
      submarineSpaces = GetSubmarineSpaces(submarineSpaceEnds);
      submarine = new Submarine(submarineSpaces);
      // alert("Submarine Spaces: " + submarineSpaces);
    }
    else
    {
      alert("Invalid syntax for gamepieces");
      return;
    }
  }

  var n;
  var m;
  for(n=0;n<aircraftSpaces.length;n++)
  {
    for(m=0;m<battleshipSpaces.length;m++)
    {
      if(aircraftSpaces[n] == battleshipSpaces[m])
      {
        alert("Game pieces cannot overlap! Check your Aircraft and Battleship placements.");
        return;
      }
    }
  }
  for(n=0;n<aircraftSpaces.length;n++)
  {
    for(m=0;m<submarineSpaces.length;m++)
    {
      if(aircraftSpaces[n] == submarineSpaces[m])
      {
        alert("Game pieces cannot overlap! Check your Aircraft and Submarine placements.");
        return;
      }
    }
  }
  for(n=0;n<battleshipSpaces.length;n++)
  {
    for(m=0;m<submarineSpaces.length;m++)
    {
      if(battleshipSpaces[n] == submarineSpaces[m])
      {
        alert("Game pieces cannot overlap! Check your Battleship and Submarine placements.");
        return;
      }
    }
  }


  if(aircraft == undefined)
  {
    alert("You need to specify all games pieces. Please include an Aircraft.");
    return;
  }
  if(battleship == undefined)
  {
    alert("You need to specify all games pieces. Please include a Battleship.");
    return;
  }
  if(submarine == undefined)
  {
    alert("You need to specify all games pieces. Please include a Submarine.");
    return;
  }

  return [aircraft, battleship, submarine];
}


function GetAircraftSpaces(spaces)
{
  var spaceArray = [];

  var space1_letter = spaces[0].charAt(0);
  var space1_number;
  if(spaces[0].length > 2)
  {
    space1_number = spaces[0].substring(1,3);
  }
  else
  {
    space1_number = spaces[0].charAt(1);
  }

  var space2_letter = spaces[1].charAt(0);
  var space2_number;
  if(spaces[1].length > 2)
  {
    space2_number = spaces[1].substring(1,3);
  }
  else
  {
    space2_number = spaces[1].charAt(1);
  }
  var s1_charCode = space1_letter.charCodeAt(0);
  var s2_charCode = space2_letter.charCodeAt(0);
  var s1_number = parseInt(space1_number);
  var s2_number = parseInt(space2_number);

  if(s1_charCode == s2_charCode)
  {
    if((s2_number - s1_number) == 4)
    {
      spaceArray.push(spaces[0]);
      var nextSpaceNum = s1_number;
      var x;
      for(x=0;x<4;x++)
      {
        nextSpaceNum++;
        spaceArray.push(space1_letter + nextSpaceNum);
      }

      return spaceArray;
    }
    else
    {
      alert("Invalid space numbers! Aircraft must be 5 spaces long.");
      return null;
    }
  }
  else if((s2_charCode - s1_charCode) == 4)
  {
    if(s1_number == s2_number)
    {
      spaceArray.push(spaces[0]);
      var nextSpaceLetter = s1_charCode;
      var x;
      for(x=0;x<4;x++)
      {
        nextSpaceLetter++;
        spaceArray.push(String.fromCharCode(nextSpaceLetter) + s1_number);
      }

      return spaceArray;
    }
    else
    {
      alert("Invalid space letters! Aircraft must be 5 spaces long.");
      return null;
    }
  }
}

function GetBattleshipSpaces(spaces)
{
  var spaceArray = [];

  var space1_letter = spaces[0].charAt(0);
  var space1_number;
  if(spaces[0].length > 2)
  {
    space1_number = spaces[0].substring(1,3);
  }
  else
  {
    space1_number = spaces[0].charAt(1);
  }

  var space2_letter = spaces[1].charAt(0);
  var space2_number;
  if(spaces[1].length > 2)
  {
    space2_number = spaces[1].substring(1,3);
  }
  else
  {
    space2_number = spaces[1].charAt(1);
  }
  var s1_charCode = space1_letter.charCodeAt(0);
  var s2_charCode = space2_letter.charCodeAt(0);
  var s1_number = parseInt(space1_number);
  var s2_number = parseInt(space2_number);

  if(s1_charCode == s2_charCode)
  {
    if((s2_number - s1_number) == 3)
    {
      spaceArray.push(spaces[0]);
      var nextSpaceNum = s1_number;
      var x;
      for(x=0;x<3;x++)
      {
        nextSpaceNum++;
        spaceArray.push(space1_letter + nextSpaceNum);
      }

      return spaceArray;
    }
    else
    {
      alert("Invalid space numbers! Battleship must be 4 spaces long.");
      return null;
    }
  }
  else if((s2_charCode - s1_charCode) == 3)
  {
    if(s1_number == s2_number)
    {
      spaceArray.push(spaces[0]);
      var nextSpaceLetter = s1_charCode;
      var x;
      for(x=0;x<3;x++)
      {
        nextSpaceLetter++;
        spaceArray.push(String.fromCharCode(nextSpaceLetter) + s1_number);
      }

      return spaceArray;
    }
    else
    {
      alert("Invalid space letters! Battleship must be 4 spaces long.");
      return null;
    }
  }
}

function GetSubmarineSpaces(spaces)
{
  var spaceArray = [];

  var space1_letter = spaces[0].charAt(0);
  var space1_number;
  if(spaces[0].length > 2)
  {
    space1_number = spaces[0].substring(1,3);
  }
  else
  {
    space1_number = spaces[0].charAt(1);
  }

  var space2_letter = spaces[1].charAt(0);
  var space2_number;
  if(spaces[1].length > 2)
  {
    space2_number = spaces[1].substring(1,3);
  }
  else
  {
    space2_number = spaces[1].charAt(1);
  }
  var s1_charCode = space1_letter.charCodeAt(0);
  var s2_charCode = space2_letter.charCodeAt(0);
  var s1_number = parseInt(space1_number);
  var s2_number = parseInt(space2_number);

  if(s1_charCode == s2_charCode)
  {
    if((s2_number - s1_number) == 2)
    {
      spaceArray.push(spaces[0]);
      var nextSpaceNum = s1_number;
      var x;
      for(x=0;x<2;x++)
      {
        nextSpaceNum++;
        spaceArray.push(space1_letter + nextSpaceNum);
      }

      return spaceArray;
    }
    else
    {
      alert("Invalid space numbers! Submarine must be 3 spaces long.");
      return null;
    }
  }
  else if((s2_charCode - s1_charCode) == 2)
  {
    if(s1_number == s2_number)
    {
      spaceArray.push(spaces[0]);
      var nextSpaceLetter = s1_charCode;
      var x;
      for(x=0;x<2;x++)
      {
        nextSpaceLetter++;
        spaceArray.push(String.fromCharCode(nextSpaceLetter) + s1_number);
      }

      return spaceArray;
    }
    else
    {
      alert("Invalid space letters! Submarine must be 3 spaces long.");
      return null;
    }
  }
}


function SetAircraft(aircraft)
{
  var space1_id = "B_" + aircraft.space1.name.toUpperCase();
  var space2_id = "B_" + aircraft.space2.name.toUpperCase();
  var space3_id = "B_" + aircraft.space3.name.toUpperCase();
  var space4_id = "B_" + aircraft.space4.name.toUpperCase();
  var space5_id = "B_" + aircraft.space5.name.toUpperCase();
  document.getElementById(space1_id).innerHTML = "A";
  document.getElementById(space2_id).innerHTML = "A";
  document.getElementById(space3_id).innerHTML = "A";
  document.getElementById(space4_id).innerHTML = "A";
  document.getElementById(space5_id).innerHTML = "A";

  if(aircraft.space1.status == "bombed")
  {
    document.getElementById(space1_id).style.backgroundColor = "red";
  }
  if(aircraft.space2.status == "bombed")
  {
    document.getElementById(space2_id).style.backgroundColor = "red";
  }
  if(aircraft.space3.status == "bombed")
  {
    document.getElementById(space3_id).style.backgroundColor = "red";
  }
  if(aircraft.space4.status == "bombed")
  {
    document.getElementById(space4_id).style.backgroundColor = "red";
  }
  if(aircraft.space5.status == "bombed")
  {
    document.getElementById(space5_id).style.backgroundColor = "red";
  }

  return;
}

function SetBattleship(battleship)
{
  var space1_id = "B_" + battleship.space1.name.toUpperCase();
  var space2_id = "B_" + battleship.space2.name.toUpperCase();
  var space3_id = "B_" + battleship.space3.name.toUpperCase();
  var space4_id = "B_" + battleship.space4.name.toUpperCase();
  document.getElementById(space1_id).innerHTML = "B";
  document.getElementById(space2_id).innerHTML = "B";
  document.getElementById(space3_id).innerHTML = "B";
  document.getElementById(space4_id).innerHTML = "B";

  if(battleship.space1.status == "bombed")
  {
    document.getElementById(space1_id).style.backgroundColor = "red";
  }
  if(battleship.space2.status == "bombed")
  {
    document.getElementById(space2_id).style.backgroundColor = "red";
  }
  if(battleship.space3.status == "bombed")
  {
    document.getElementById(space3_id).style.backgroundColor = "red";
  }
  if(battleship.space4.status == "bombed")
  {
    document.getElementById(space4_id).style.backgroundColor = "red";
  }

  return;
}

function SetSubmarine(submarine)
{
  var space1_id = "B_" + submarine.space1.name.toUpperCase();
  var space2_id = "B_" + submarine.space2.name.toUpperCase();
  var space3_id = "B_" + submarine.space3.name.toUpperCase();
  document.getElementById(space1_id).innerHTML = "S";
  document.getElementById(space2_id).innerHTML = "S";
  document.getElementById(space3_id).innerHTML = "S";

  if(submarine.space1.status == "bombed")
  {
    document.getElementById(space1_id).style.backgroundColor = "red";
  }
  if(submarine.space2.status == "bombed")
  {
    document.getElementById(space2_id).style.backgroundColor = "red";
  }
  if(submarine.space3.status == "bombed")
  {
    document.getElementById(space3_id).style.backgroundColor = "red";
  }

  return;
}

function SetMissed()
{
  var bottomID;
  if(currentPlayer == 1)
  {
    var z;
    for(z=0;z<missedHits1.length;z++)
    {
      // alert("Missed Hit: " + missedHits1[z]);
      document.getElementById(missedHits1[z]).style.backgroundColor = "white";
    }
    var a;
    for(a=0;a<missedHits2.length;a++)
    {
      bottomID = "B_" + missedHits2[a].split("_")[1]
      document.getElementById(bottomID).style.backgroundColor = "white";
    }
  }
  else if(currentPlayer == 2)
  {
    var z;
    for(z=0;z<missedHits2.length;z++)
    {
      // alert("Missed Hit: " + missedHits2[z]);
      document.getElementById(missedHits2[z]).style.backgroundColor = "white";
    }
    var a;
    for(a=0;a<missedHits1.length;a++)
    {
      bottomID = "B_" + missedHits1[a].split("_")[1]
      document.getElementById(bottomID).style.backgroundColor = "white";
    }
  }

  return;
}

function SetBombed()
{
  if(currentPlayer == 1)
  {
    var w;
    for(w=0;w<bombedHits1.length;w++)
    {
      document.getElementById(bombedHits1[w]).style.backgroundColor = "red";
    }
  }
  else if(currentPlayer == 2)
  {
    var w;
    for(w=0;w<bombedHits2.length;w++)
    {
      document.getElementById(bombedHits2[w]).style.backgroundColor = "red";
    }
  }

  return;
}

function GetRemainingAircraftSpaces(ship)
{
    var remaining = [];
    var notSunk = false;
    if(ship.space1.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space1.name);
    } 
    if(ship.space2.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space2.name);
    }
    if(ship.space3.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space3.name);
    }  
    if(ship.space4.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space4.name);
    }
    if(ship.space5.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space5.name);
    }
    
    if(!notSunk)
    {
        return null;
    }
    // alert(remaining);
    return remaining;
}

function GetRemainingBattleshipSpaces(ship)
{
    var remaining = [];
    var notSunk = false;
    if(ship.space1.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space1.name);
    } 
    if(ship.space2.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space2.name);
    }
    if(ship.space3.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space3.name);
    }  
    if(ship.space4.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space4.name);
    }
    
    if(!notSunk)
    {
        return null;
    }
    
    return remaining;
}

function GetRemainingSubmarineSpaces(ship)
{
    var remaining = [];
    var notSunk = false;
    if(ship.space1.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space1.name);
    } 
    if(ship.space2.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space2.name);
    }
    if(ship.space3.status == "safe")
    {
        notSunk = true;
        remaining.push(ship.space3.name);
    }  
    
    if(!notSunk)
    {
        return null;
    }
    return remaining;
}

function DisplayScores()
{
    var player1Total = player1Score - player2Score;
    if(player1Total >= 0)
        document.getElementById("player1-score").innerHTML = player1Total;
    else
        document.getElementById("player1-score").innerHTML = 0;
    
    var player2Total = player2Score - player1Score;
    if(player2Total >= 0)
        document.getElementById("player2-score").innerHTML = player2Total;
    else
        document.getElementById("player2-score").innerHTML = 0;
}


function ShotFired()
{
  var firedSpace = lockedIn.split("_")[1].toLowerCase();
  var tempPlayer = currentPlayer;
  var hitStatus = false;
  if(tempPlayer == 1)
  {
      
    // alert(aircraft2.space1.name);
    if(aircraft2.shipStatus != "sunk")
    {
        if(firedSpace == aircraft2.space1.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          // alert("Hit status: " + hitStatus);
          aircraft2.space1.status = "bombed";
          // alert("Space status: " + aircraft2.space1.status);
          bombedHits1.push(lockedIn);
          // alert("Bombed hits: " + bombedHits1);
          player1Score = player1Score + 2;
          // alert("Player Score: " + player1Score);
          if(GetRemainingAircraftSpaces(aircraft2) == null)
          {
              // alert(GetRemainingAircraftSpaces(aircraft2));
              aircraft2.shipStatus = "sunk";
              // alert(aircraft2.shipStatus);
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
        else if(firedSpace == aircraft2.space2.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft2.space2.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingAircraftSpaces(aircraft2) == null)
          {
              aircraft2.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
        else if(firedSpace == aircraft2.space3.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft2.space3.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingAircraftSpaces(aircraft2) == null)
          {
              aircraft2.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
        else if(firedSpace == aircraft2.space4.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft2.space4.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingAircraftSpaces(aircraft2) == null)
          {
              aircraft2.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
        else if(firedSpace == aircraft2.space5.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft2.space5.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingAircraftSpaces(aircraft2) == null)
          {
              aircraft2.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
    }
    if(battleship2.shipStatus != "sunk")
    {
        if(firedSpace == battleship2.space1.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          battleship2.space1.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingBattleshipSpaces(battleship2) == null)
          {
              battleship2.shipStatus = "sunk";
              alert("You've sunk the enemy's battleship!");
          }
        }
        else if(firedSpace == battleship2.space2.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          battleship2.space2.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingBattleshipSpaces(battleship2) == null)
          {
              battleship2.shipStatus = "sunk";
              alert("You've sunk the enemy's battleship!");
          }
        }
        else if(firedSpace == battleship2.space3.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          battleship2.space3.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingBattleshipSpaces(battleship2) == null)
          {
              battleship2.shipStatus = "sunk";
              alert("You've sunk the enemy's battleship!");
          }
        }
        else if(firedSpace == battleship2.space4.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          battleship2.space4.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingBattleshipSpaces(battleship2) == null)
          {
              battleship2.shipStatus = "sunk";
              alert("You've sunk the enemy's battleship!");
          }
        }
    }
    
    if(submarine2.shipStatus != "sunk")
    {
        if(firedSpace == submarine2.space1.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          submarine2.space1.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingSubmarineSpaces(submarine2) == null)
          {
              submarine2.shipStatus = "sunk";
              alert("You've sunk the enemy's submarine!");
          }
        }
        else if(firedSpace == submarine2.space2.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          submarine2.space2.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingSubmarineSpaces(submarine2) == null)
          {
              submarine2.shipStatus = "sunk";
              alert("You've sunk the enemy's submarine!");
          }
        }
        else if(firedSpace == submarine2.space3.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          submarine2.space3.status = "bombed";
          bombedHits1.push(lockedIn);
          player1Score = player1Score + 2;
          if(GetRemainingSubmarineSpaces(submarine2) == null)
          {
              submarine2.shipStatus = "sunk";
              alert("You've sunk the enemy's submarine!");
          }
        }
        
    }
    
    if(!hitStatus)
    {
      alert("Miss!");
      missedHits1.push(lockedIn);
    }
    
    if((submarine2.shipStatus == "sunk") && (aircraft2.shipStatus == "sunk") && (battleship2.shipStatus) == "sunk")
    {
		player1Score = player1Score - player2Score;
        alert("Congratulations, " + name1 + "! You won! Your total score was " + player1Score);
        SaveScore(name1,player1Score-player2Score);
        return;
    }
    
    
    ClearGameBoard("T");
    ClearGameBoard("B");
    currentPlayer = 2;
    lockedIn = null;
    document.getElementById('player1-fire').disabled = true;
    document.getElementById('startpage').style.display='block';
    document.getElementById('start-label').innerHTML = name2 + ", it's your turn!";

  }
  else if(tempPlayer == 2)
  {
    if(aircraft1.shipStatus != "sunk")
    {
        if(firedSpace == aircraft1.space1.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft1.space1.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingAircraftSpaces(aircraft1) == null)
          {
              alert(GetRemainingAircraftSpaces(aircraft1));
              aircraft1.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
        else if(firedSpace == aircraft1.space2.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft1.space2.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingAircraftSpaces(aircraft1) == null)
          {
              aircraft1.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
        else if(firedSpace == aircraft1.space3.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft1.space3.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingAircraftSpaces(aircraft1) == null)
          {
              aircraft1.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
        else if(firedSpace == aircraft1.space4.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft1.space4.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingAircraftSpaces(aircraft1) == null)
          {
              aircraft1.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
        else if(firedSpace == aircraft1.space5.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          aircraft1.space5.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingAircraftSpaces(aircraft1) == null)
          {
              aircraft1.shipStatus = "sunk";
              alert("You've sunk the enemy's aircraft carrier!");
          }
        }
    }
    if(battleship1.shipStatus != "sunk")
    {
        if(firedSpace == battleship1.space1.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          battleship1.space1.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingBattleshipSpaces(battleship1) == null)
          {
              battleship1.shipStatus = "sunk";
              alert("You've sunk the enemy's battleship!");
          }
        }
        else if(firedSpace == battleship1.space2.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          battleship1.space2.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingBattleshipSpaces(battleship1) == null)
          {
              battleship1.shipStatus = "sunk";
              alert("You've sunk the enemy's battleship!");
          }
        }
        else if(firedSpace == battleship1.space3.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          battleship1.space3.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingBattleshipSpaces(battleship1) == null)
          {
              battleship1.shipStatus = "sunk";
              alert("You've sunk the enemy's battleship!");
          }
        }
        else if(firedSpace == battleship1.space4.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          battleship1.space4.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingBattleshipSpaces(battleship1) == null)
          {
              battleship1.shipStatus = "sunk";
              alert("You've sunk the enemy's battleship!");
          }
        }
    }
    
    if(submarine1.shipStatus != "sunk")
    {
        if(firedSpace == submarine1.space1.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          submarine1.space1.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingSubmarineSpaces(submarine1) == null)
          {
              submarine1.shipStatus = "sunk";
              alert("You've sunk the enemy's submarine!");
          }
        }
        else if(firedSpace == submarine1.space2.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          submarine1.space2.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingSubmarineSpaces(submarine1) == null)
          {
              submarine1.shipStatus = "sunk";
              alert("You've sunk the enemy's submarine!");
          }
        }
        else if(firedSpace == submarine1.space3.name)
        {
          alert("Direct hit!");
          hitStatus = true;
          submarine1.space3.status = "bombed";
          bombedHits2.push(lockedIn);
          player2Score = player2Score + 2;
          if(GetRemainingSubmarineSpaces(submarine1) == null)
          {
              submarine1.shipStatus = "sunk";
              alert("You've sunk the enemy's submarine!");
          }
        }
    }
    
    if(!hitStatus)
    {
      alert("Miss!");
      missedHits2.push(lockedIn);
    }
    
    
    if((submarine1.shipStatus == "sunk") && (aircraft1.shipStatus == "sunk") && (battleship1.shipStatus == "sunk"))
    {
		player2Score = player2Score - player1Score;
        alert("Congratulations, " + name2 + "! You won! Your total score was " + player2Score);
        SaveScore(name2,player2Score);
        return;
    }
    
    ClearGameBoard("T");
    ClearGameBoard("B");
    currentPlayer = 1;
    lockedIn = null;
    document.getElementById('player2-fire').disabled = true;
    document.getElementById('startpage').style.display='block';
    document.getElementById('start-label').innerHTML = name1 + ", it's your turn!";
  }
  DisplayScores();
  
  
  
}

function ChangeBG(bgColor, elementID)
{
  document.getElementById(elementID).style.backgroundColor = bgColor;
}

function LockIn(elementID)
{
  if(currentPlayer == 1)
  {
      if(contains(bombedHits1,elementID))
      {
          alert("You cannot select a bombed position! Please choose another fire location.");
          return;
      }
	  else if(contains(missedHits1,elementID))
	  {
		  alert("You cannot select a previously selected position! Please choose another fire location.");
          return;
	  }
  }
  else
  {
      if(contains(bombedHits2,elementID))
      {
          alert("You cannot select a bombed position! Please choose another fire location.");
          return;
      }
	  else if(contains(missedHits2,elementID))
	  {
		  alert("You cannot select a previously selected position! Please choose another fire location.");
          return;
	  }
  }
  if(lockedIn == null)
  {
    lockedIn = elementID;
    document.getElementById(elementID).style.backgroundColor = "#003366";
    // document.getElementById(elementID).onmouseout = "";
    // document.getElementById(elementID).onmouseover = "";
    if(currentPlayer == 1)
    {
      document.getElementById('player1-fire').disabled = false;
    }
    else if(currentPlayer == 2)
    {
      document.getElementById('player2-fire').disabled = false;
    }
  }
  else if(lockedIn == elementID)
  {
    UnLock(elementID);
  }
  else
  {
    alert("You can only fire at one location per turn. Please unlock your previous selection to choose another fire location.");
  }

}

function UnLock(elementID)
{
  if(lockedIn == elementID)
  {
    lockedIn = null;
    document.getElementById(elementID).style.backgroundColor = "#bfefff";
    if(currentPlayer == 1)
    {
      document.getElementById('player1-fire').disabled = true;
    }
    else if(currentPlayer == 2)
    {
      document.getElementById('player2-fire').disabled = true;
    }
    // document.getElementById(elementID).onmouseover = "ChangeBG('PaleGreen', 'T_A1');";
    // document.getElementById(elementID).onmouseout = "ChangeBG('bfefff','T_A1');";
  }

}

function SaveScore(playerName, playerScore)
{
    var savedScores = [];
    var savedNames = [];
    

    if(localStorage.length != 0)
    {
        for(var k=0; k<localStorage.length;k++)
        {
            savedNames.push[localStorage.key(k)];
            savedScores.push[localStorage.getItem(localStorage.key(k))]
        }
        
        if(savedScores.length < 10)
        {
            for(var j=0; j<savedScores.length;j++)
            {
                if(playerScore > savedScores[j])
                {
                    savedScores.shift(playerScore);
                    savedNames.shift(playerName);
                    localStorage.clear();
                    for(var n=0; n<savedScores.length;n++)
                    {
                        localStorage.setItem(savedNames[n],savedScores[n]);
                    }
                    break;
                }
				else
				{
					localStorage.setItem(playerName, playerScore);
				}
            }
        }
        else if(savedScores.length == 10)
        {
            for(var k=0; k<savedScores.length;k++)
            {
                if(playerScore > savedScores[k])
                {
                    savedScores.shift(playerScore);
                    savedNames.shift(playerName);
                    localStorage.clear();
                    for(var n=0; n<10;n++)
                    {
                        var m=n+1;
                        localStorage.setItem(savedNames[n],savedScores[n]);
                    }
                    break;
                }
            }
        }
    }
        
    
    else
    {
        localStorage.setItem(playerName, playerScore);
    }
}

function contains(findIn, item)
{
   for(var i=0; i<findIn.length; i++)
   {
       if(item == findIn[i])
       {
           return true;
       }
   }

    return false;
}