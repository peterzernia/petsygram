function toggleFollow(){
      $.ajax({
        url: window.USER_FOLLOW_URL,
        success: function(data) {
          $("#followCount").html(data.follower_count + ' Followers');
          $('#followElement').html(data.button);
        }
      });
};

function "window.POST_ID"(){
      $.ajax({
        url: window.USER_LIKE_URL,
        success: function(data) {
          $("#likeCount" + window.POST_ID).html(data.like_count + ' likes');
          $("#imageElement" + window.POST_ID).html(data.img);
          console.log(data);
        },
        error: function(error) {
          console.log(error);
        }
        });
    };
