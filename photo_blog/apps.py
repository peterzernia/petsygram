from django.apps import AppConfig


class PhotoBlogConfig(AppConfig):
    name = 'photo_blog'

    def ready(self):
        import photo_blog.signals
