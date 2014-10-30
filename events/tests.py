from django.test import TestCase
import re

class YoutubeTest(TestCase):
    """Test Youtube Pattern to get video id."""

    def setUp(self):
        """docstring for setUp"""
        self.video_id_pattern = re.compile(r"""^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??(v=)?([0-9a-zA-Z\-_]+).*$""")
        self.GROUP_VIDEO_ID = 8

    def test_iframe(self):
        """Test iframe link."""
        youtube_links = {
                'GSmvWyTJLYE' : '<iframe width="635" height="357" src="//www.youtube.com/embed/GSmvWyTJLYE" frameborder="0" allowfullscreen></iframe>',
                'TwIh_i-kGxg' : '<iframe width="635" height="357" src="//www.youtube.com/embed/TwIh_i-kGxg" frameborder="0" allowfullscreen></iframe>',
                'TxypVAeGGI4' : '<iframe width="635" height="357" src="//www.youtube.com/embed/TxypVAeGGI4" frameborder="0" allowfullscreen></iframe>',
                'lg7RokKcAKY' : '<iframe width="635" height="357" src="//www.youtube.com/embed/lg7RokKcAKY" frameborder="0" allowfullscreen></iframe>',
                'TU_RBabWBkE' : '<iframe width="635" height="357" src="//www.youtube.com/embed/TU_RBabWBkE" frameborder="0" allowfullscreen></iframe>',
                'ksSyVz1tI3Y' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/ksSyVz1tI3Y" frameborder="0" allowfullscreen></iframe>',
                'vXtJkDHEAAc' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/vXtJkDHEAAc" frameborder="0" allowfullscreen></iframe>',
                'HG6kim3oy8M' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/HG6kim3oy8M" frameborder="0" allowfullscreen></iframe>',
                'YOgOc1QjLlY' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/YOgOc1QjLlY?rel=0" frameborder="0" allowfullscreen></iframe>',
                'eYfkTD9odTA' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/eYfkTD9odTA?rel=0" frameborder="0" allowfullscreen></iframe>',
                'UlRVmQcPraU' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/UlRVmQcPraU" frameborder="0" allowfullscreen></iframe>',
                'fIw8QvbiHbg' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/fIw8QvbiHbg" frameborder="0" allowfullscreen></iframe>',
                'wX08w4f3T0Y' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/wX08w4f3T0Y" frameborder="0" allowfullscreen></iframe>',
                'cpe1kpVc40M' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/cpe1kpVc40M?rel=0" frameborder="0" allowfullscreen></iframe>',
                'U0R82n1E7Uw' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/U0R82n1E7Uw?rel=0" frameborder="0" allowfullscreen></iframe>',
                't-UCjotRmMY' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/t-UCjotRmMY?rel=0" frameborder="0" allowfullscreen></iframe>',
                'hjHf6NKI-R0' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/hjHf6NKI-R0?rel=0" frameborder="0" allowfullscreen></iframe>',
                'a5fHoAx12DY' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/a5fHoAx12DY?rel=0" frameborder="0" allowfullscreen></iframe>',
                'Q7lKOzOh0Kg' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/Q7lKOzOh0Kg?rel=0" frameborder="0" allowfullscreen></iframe>',
                'H2F1yi8J59Y' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/H2F1yi8J59Y?rel=0" frameborder="0" allowfullscreen></iframe>',
                'L7Jx-VHxMEU' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/L7Jx-VHxMEU?rel=0" frameborder="0" allowfullscreen></iframe>',
                '64W80SUSt4c' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/64W80SUSt4c?rel=0" frameborder="0" allowfullscreen></iframe>',
                '2R9-MA462h0' : '<iframe width="635" height="357" src="http://www.youtube.com/embed/2R9-MA462h0?rel=0" frameborder="0" allowfullscreen></iframe>'
        }
        for video_id in youtube_links.keys():
            youtube_video_id = self.video_id_pattern.match(youtube_links.get(video_id))
            print("%s-%s" %(video_id, youtube_video_id.group(self.GROUP_VIDEO_ID)))
            self.assertEqual(youtube_video_id.group(self.GROUP_VIDEO_ID), video_id)

    def test_user_link(self):
        """Test for youtube user link."""
        youtube_user_links = {
                '6dwqZw0j_jY' : 'http://www.youtube.com/user/SilkRoadTheatre#p/a/u/2/6dwqZw0j_jY',
                '1p3vcRhsYGo' : 'http://www.youtube.com/user/Scobleizer#p/u/1/1p3vcRhsYGo'
        }
        for video_id in youtube_user_links:
            youtube_video_id = self.video_id_pattern.match(youtube_user_links.get(video_id))
            self.assertEqual(youtube_video_id.group(self.GROUP_VIDEO_ID), video_id)

    def test_short_link(self):
        """Test for short link."""
        youtube_short_links ={ 
                '6dwqZw0j_jY' : 'http://youtu.be/6dwqZw0j_jY',
                'afa-5HQHiAs' : 'http://youtu.be/afa-5HQHiAs',
                '-wtIMTCHWuI' : 'http://youtu.be/-wtIMTCHWuI'

        } 
        for video_id in youtube_short_links:
            youtube_video_id = self.video_id_pattern.match(youtube_short_links.get(video_id))
            self.assertEqual(youtube_video_id.group(self.GROUP_VIDEO_ID), video_id)

    def test_watch_link(self):
        """Test for watch link."""
        youtube_watch_links = {
                'cKZDdG9FTKY' : 'http://www.youtube.com/watch?v=cKZDdG9FTKY&feature=channel',
                'yZ-K7nCVnBI' : 'http://www.youtube.com/watch?v=yZ-K7nCVnBI&playnext_from=TL&videos=osPknwzXEas&feature=sub',
                '6dwqZw0j_jY' : 'http://www.youtube.com/watch?v=6dwqZw0j_jY&feature=youtu.be',
                '-wtIMTCHWuI' : 'http://www.youtube.com/watch?v=-wtIMTCHWuI',
                '-wtIMTCHWuI' : 'http://www.youtube.com/v/-wtIMTCHWuI?version=3&autohide=1'
        }
        for video_id in youtube_watch_links:
            youtube_video_id = self.video_id_pattern.match(youtube_watch_links.get(video_id))
            self.assertEqual(youtube_video_id.group(self.GROUP_VIDEO_ID), video_id)
