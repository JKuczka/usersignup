#!/usr/bin/env python
#
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cgi                                                                      # imports
import re
import webapp2
                                                                                # header
header = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>
                Signup
            </title>
            <style>
                .error {
                    color:red;
                }
                #welcome {
                    margin-top:100px;
                    text-align:center;
                    font-weight:normal;
                }
            </style>
        </head>
        <body>
"""
                                                                                # footer
footer = """
        </body>
    </html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")                                  # regex for variables
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")                                   # email works without '.someletters'

def validUsername(username):                                                    # validation
    return USER_RE.match(username)

def validPassword(password):
    return PASSWORD_RE.match(password)

def validEmail(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):                                      # signup page
    def get(self):
        error_username = self.request.get("error1")                             # initializing variables
        error_pass = self.request.get("error2")
        error_verify = self.request.get("error3")
        error_email = self.request.get("error4")
        username = self.request.get("username")
        email = self.request.get("email")
        pageTop = """
            <div id="holder">
                <h1>Signup</h1>
        """
                                                                                # main form
        form = """
            <form action="/welcome" method="post">
                <label for="username">Username</label>
                <input name="username" type="text" value="{0}" />
                <span class="error">{1}</span><br>
                <label for="password">Password</label>
                <input name="password" type="password" />
                <span class="error">{2}</span><br>
                <label for="verify">Verify Password</label>
                <input name="verify" type="password" />
                <span class="error">{3}</span><br>
                <label for="email">Email (Optional)</label>
                <input name="email" type="email" value="{4}" />
                <span class="error">{5}</span><br>
                <input type="submit" value="Submit" />
            </form>
        """.format(username, error_username, error_pass, error_verify, email, error_email)
        pageBottom = """
            </div>
        """

        page = pageTop + form + pageBottom
        content = header + page + footer
        self.response.write(content)                                            # display content

class WelcomeHandler(webapp2.RequestHandler):                                   # welcome page
    def post(self):
        username = self.request.get("username")                                 # initialize variables
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        usernameValid = False
        passwordValid = False
        verifyValid = False
        emailValid = False
        form_error = ["", "", "", ""]                                           # list for errors

        if validUsername(username):                                             # adding error messages if needed
            usernameValid = True
        else:
            form_error[0] = "Invalid username"

        if validPassword(password):
            passwordValid = True
        else:
            form_error[1] = "Invalid password"

        if verify == password:
            verifyValid = True
        else:
            form_error[2] = "Passwords do not match"

        if email != "":
            if validEmail(email):
                emailValid = True
            else:
                form_error[3] = "Invalid email"
        else:
            emailValid = True

        error = "?"                                                             # setting up to pass errors
        first = True
        for i in range(len(form_error)):
            if form_error[i] != "":
                if first == False:
                    error += "&error{0}={1}".format(i + 1, form_error[i])
                else:
                    error += "error{0}={1}".format(i + 1, form_error[i])
                    first = False

        preserve = ""                                                           # setting up to preserve username and email

        if not username == "" and not email == "":
            preserve += "&username={0}&email={1}".format(username, email)
        elif not username == "":
            preserve += "&username={}".format(username)
        else:
            preserve += "&email={}".format(email)

        if not error == "?":
            self.redirect("/{0}{1}".format(error, preserve))
                                                                                # welcome page display
        welcome_header = """
            <h1 id="welcome">Welcome, {}!</h1>
        """.format(cgi.escape(username, quote=True))

        content = header + welcome_header + footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
