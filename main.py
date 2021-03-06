import webapp2

from libs.utils import make_secure_val, check_secure_val
from blog import BlogHandler
from blog import Signup, Login, Logout, Welcome, FlushMemcache
from blog import BlogFront, PostPage, NewPost
from rot13 import Rot13


class MainPage(BlogHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')

        if visit_cookie_str:
            cookie_val = check_secure_val(visit_cookie_str)
            if cookie_val:
                visits = int(cookie_val)

        # if cookie is invalid, visits will be set back to 1
        visits += 1

        new_cookie_val = make_secure_val(str(visits))

        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
        
        if visits > 10000:
            self.write("You are the best ever!")
        else:
            self.write("You've been here %s times!" % visits)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rot13', Rot13),
                               ('/blog/signup', Signup),
                               ('/blog/login', Login),
                               ('/blog/logout', Logout),
                               ('/welcome', Welcome),
                               ('/blog/?(?:\.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:\.json)?', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/flush', FlushMemcache),
                               ],
                              debug=True)
