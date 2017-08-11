window.onload = function(){
  checkStatus();
  $("#passphrase").keypress(function(e) {
     if (e.which == 13) {
         tryToggle(e)
     }
  });
  $("#submitButton").click(tryToggle)

}

function tryToggle(event) {
  event.preventDefault();
  $.post("/tryToggle", JSON.stringiy({passphrase: $("#passphrase").val()}) , function (response) {
    if(response.status === "ok")
      checkStatus();
    else
      alert("wrong passphrase")
  })
}

function checkStatus(){
  $.get("/getStatus", function(response){
    $("#statusicon").removeClass();
    if(response === "off"){
      $("#statusicon").addClass("glyphicon glyphicon-off");
      $("#statusicon").text(" Off")
    }
    else{
      $("#statusicon").addClass("glyphicon glyphicon-thumbs-up");
      $("#statusicon").text(" On")
    }
  })
}
