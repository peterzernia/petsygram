function toggleFollow(){
      $.ajax({
        url: window.USER_FOLLOW_URL,
        success: function(data) {
          $("#followCount").html(data.follower_count + ' Followers');
          $('#followElement').html(data.button);
        }
      });
};


function toggleLike(post_id){
      $.ajax({
        url: "/post/" + post_id + "/like_api",
        success: function(data) {
          $("#likeCount" + post_id).html(data.like_count + ' likes');
          $("#imageElement" + post_id).html(data.img);
        }
      });
};
