function toggleFollow(){
      $.ajax({
        url: "{% url 'user_follow' view.kwargs.username %}",
        success: function(data) {
          $("#followCount").html(data.follower_count + ' Followers');
          $('#followElement').html(data.button);
        }
      });
};
