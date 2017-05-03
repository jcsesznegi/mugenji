function urlGetParameter(url, name)
{
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(url);
  if(results == null) {
      return "";
  } else {
      return results[1];
  }
}

function userAddKanji(kanji) {
  $("#card_content_" + kanji).toggle("blind", {}, 200);
  $.ajax({
      url: "/user/addkanji",
      global: false,
      cache: false,
      type: "POST",
      data: "kanji="+kanji,
      dataType: "html",
      async: true,
      success: function(){
          $("#card_" + kanji).addClass("card_closed");
          $("#card_top_" + kanji).addClass("card_top_closed");
          $("#content_sub").load("/user/stats");
      }
  });
}

function userDeleteKanji(kanji) {
  $.ajax({
      url: "/user/deletekanji",
      global: false,
      cache: false,
      type: "POST",
      data: "kanji="+kanji,
      dataType: "html",
      async: true,
      success: function(){
          $("#card_" + kanji).removeClass("card_closed");
          $("#card_top_" + kanji).removeClass("card_top_closed");
          $("#content_sub").load("/user/stats");
      }
  });
  $("#card_content_" + kanji).toggle("blind", {}, 200);
}



