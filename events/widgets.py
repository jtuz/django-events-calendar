from django.contrib.admin.widgets import AdminFileWidget, AdminTextInputWidget
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from PIL import Image
import os


class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            # defining the size
            size = '200x200'
            x, y = [int(x) for x in size.split('x')]
            try:
                # defining the filename and the miniature filename
                filehead, filetail = os.path.split(value.path)
                basename, format = os.path.splitext(filetail)
                miniature = basename + '_' + size + format
                filename = value.path
                miniature_filename = os.path.join(filehead, miniature)
                filehead, filetail = os.path.split(value.url)
                miniature_url = filehead + '/' + miniature

                # make sure that the thumbnail is a version of the current original sized image
                if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
                    os.unlink(miniature_filename)

                # if the image wasn't already resized, resize it
                if not os.path.exists(miniature_filename):
                    image = Image.open(filename)
                    image.thumbnail([x, y], Image.ANTIALIAS)
                    try:
                        image.save(miniature_filename, image.format, quality=100, optimize=1)
                    except:
                        image.save(miniature_filename, image.format, quality=100)

                output.append(u' <div><a href="%s" target="_blank"><img src="%s" alt="%s" /></a></div>' %
                             (miniature_url, miniature_url, miniature_filename))
            except IOError:
                pass
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class AdminYoutubeWidget(AdminTextInputWidget):
    """
    A TextInput Widget that displays an embeded youtube video
    instead of a simple Text Input field.
    """
    def render(self, name, value, attrs=None):
        import re
        EMBED_HTML = """<div><iframe src="http://www.youtube.com/embed/%s?rel=0"
                        width="400" height="200" frameborder></iframe></div>
                     """
        youtube_id_pattern = re.compile(r"""^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([0-9a-zA-Z\-_]+).*$""")
        output = []
        if value:
            match_obj = youtube_id_pattern.search(str(value))
            if match_obj.group(7) is not None:
                youtube_id = match_obj.group(7)
                output.append(EMBED_HTML % youtube_id)
            else:
                output.append("<b>%s</b>" % _('This is not a valid youtube link'))
        output.append(super(AdminTextInputWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
