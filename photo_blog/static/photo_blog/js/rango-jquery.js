function toggleLike(){
    $.ajax({
      url: "{% url 'photo_blog-post_like_api' post.id %}",
      data: {like_count: 'like_count', 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      dataType: "json",
      success: function(data) {
        $("#likeCount").html(data.like_count + ' likes');
        $('#ImageElement').replaceWith(data.img)
        console.log(data);
      }
    });
};
