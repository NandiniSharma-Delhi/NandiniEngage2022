
var arr;

// arr stores the song data mapped by id


var players = document.getElementsByClassName("playerlink");
for(var i = 0, len = players.length; i < len; i++){
  // to play the clicked song
  //to play a song first stop the music player then wait for some seconds .then click on play button of the song to play next
  players[i].addEventListener('click', function(element){

    console.log(arr.has(element.target.id));
    var varlist= arr.get(element.target.id);
    console.log(varlist);
    document.getElementById("musicplayer1").src = varlist[0];
    document.getElementById("musicplayer2").innerHTML = varlist[3];
    document.getElementById("musicplayer5").innerHTML = varlist[1];
    document.getElementById("musicplayer3").src = varlist[2];
    document.getElementById("musicplayer4").load();
  
  });
}
