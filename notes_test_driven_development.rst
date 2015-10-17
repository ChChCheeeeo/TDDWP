# Test-Driven Development with Python

- http://shop.oreilly.com/product/110000781.do?cmp=yt-prog-books-videos-product-promo_test_driven_development
- https://www.youtube.com/user/OreillyMedia
- chimera.labs.oreilly.com/books/1234000000754/index.html
- https://github.com/hjwp/book-example/

Table of Contents

    Preface
        Why I Wrote a Book About Test-Driven Development
        Aims of This Book
        Outline
        Conventions Used in This Book
        Using Code Examples
        Safari® Books Online
        Contacting O’Reilly
    Prerequisites and Assumptions
        Python 3 and Programming
        How HTML Works
        JavaScript
        Required Software Installations
            Git’s Default Editor, and Other Basic Git Config
            Required Python Packages
    Companion Video
    Acknowledgments
    I. The Basics of TDD and Django
        1. Getting Django Set Up Using a Functional Test
            Obey the Testing Goat! Do Nothing Until You Have a Test
            Getting Django Up and Running
            Starting a Git Repository
        2. Extending Our Functional Test Using the unittest Module
            Using a Functional Test to Scope Out a Minimum Viable App
            The Python Standard Library’s unittest Module
            Implicit waits
            Commit
        3. Testing a Simple Home Page with Unit Tests
            Our First Django App, and Our First Unit Test
            Unit Tests, and How They Differ from Functional Tests
            Unit Testing in Django
            Django’s MVC, URLs, and View Functions
            At Last! We Actually Write Some Application Code!
            urls.py
            Unit Testing a View
                The Unit-Test/Code Cycle
        4. What Are We Doing with All These Tests?
            Programming Is like Pulling a Bucket of Water up from a Well
            Using Selenium to Test User Interactions
            The “Don’t Test Constants” Rule, and Templates to the Rescue
                Refactoring to Use a Template
            On Refactoring
            A Little More of Our Front Page
            Recap: The TDD Process
        5. Saving User Input
            Wiring Up Our Form to Send a POST Request
            Processing a POST Request on the Server
            Passing Python Variables to Be Rendered in the Template
            Three Strikes and Refactor
            The Django ORM and Our First Model
                Our First Database Migration
                The Test Gets Surprisingly Far
                A New Field Means a New Migration
            Saving the POST to the Database
            Redirect After a POST
                Better Unit Testing Practice: Each Test Should Test One Thing
            Rendering Items in the Template
            Creating Our Production Database with migrate
        6. Getting to the Minimum Viable Site
            Ensuring Test Isolation in Functional Tests
                Running Just the Unit Tests
            Small Design When Necessary
                YAGNI!
                REST
            Implementing the New Design Using TDD
            Iterating Towards the New Design
            Testing Views, Templates, and URLs Together with the Django Test Client
                A New Test Class
                A New URL
                A New View Function
                A Separate Template for Viewing Lists
            Another URL and View for Adding List Items
                A Test Class for New List Creation
                A URL and View for New List Creation
                Removing Now-Redundant Code and Tests
                Pointing Our Forms at the New URL
            Adjusting Our Models
                A Foreign Key Relationship
                Adjusting the Rest of the World to Our New Models
            Each List Should Have Its Own URL
                Capturing Parameters from URLs
                Adjusting new_list to the New World
            One More View to Handle Adding Items to an Existing List
                Beware of Greedy Regular Expressions!
                The Last New URL
                The Last New View
                But How to Use That URL in the Form?
            A Final Refactor Using URL includes
    II. Web Development Sine Qua Nons
        7. Prettification: Layout and Styling, and What to Test About It
            What to Functionally Test About Layout and Style
            Prettification: Using a CSS Framework
            Django Template Inheritance
            Integrating Bootstrap
                Rows and Columns
            Static Files in Django
                Switching to StaticLiveServerTestCase
            Using Bootstrap Components to Improve the Look of the Site
                Jumbotron!
                Large Inputs
                Table Styling
            Using Our Own CSS
            What We Glossed Over: collectstatic and Other Static Directories
            A Few Things That Didn’t Make It
        8. Testing Deployment Using a Staging Site
            TDD and the Danger Areas of Deployment
            As Always, Start with a Test
            Getting a Domain Name
            Manually Provisioning a Server to Host Our Site
                Choosing Where to Host Our Site
                Spinning Up a Server
                User Accounts, SSH, and Privileges
                Installing Nginx
                Configuring Domains for Staging and Live
                Using the FT to Confirm the Domain Works and Nginx Is Running
            Deploying Our Code Manually
                Adjusting the Database Location
                Creating a Virtualenv
                Simple Nginx Configuration
                Creating the Database with migrate
            Getting to a Production-Ready Deployment
                Switching to Gunicorn
                Getting Nginx to Serve Static Files
                Switching to Using Unix Sockets
                Switching DEBUG to False and Setting ALLOWED_HOSTS
                Using Upstart to Make Sure Gunicorn Starts on Boot
                Saving Our Changes: Adding Gunicorn to Our requirements.txt
            Automating
                "Saving Your Progress"
        9. Automating Deployment with Fabric
            Breakdown of a Fabric Script for Our Deployment
            Trying It Out
                Deploying to Live
                Nginx and Gunicorn Config Using sed
            Git Tag the Release
            Further Reading
        10. Input Validation and Test Organisation
            Validation FT: Preventing Blank Items
                Skipping a Test
                Splitting Functional Tests out into Many Files
                Running a Single Test File
                Fleshing Out the FT
            Using Model-Layer Validation
                Refactoring Unit Tests into Several Files
                Unit Testing Model Validation and the self.assertRaises Context Manager
                A Django Quirk: Model Save Doesn’t Run Validation
            Surfacing Model Validation Errors in the View
                Checking Invalid Input Isn’t Saved to the Database
            Django Pattern: Processing POST Requests in the Same View as Renders the Form
                Refactor: Transferring the new_item Functionality into view_list
                Enforcing Model Validation in view_list
            Refactor: Removing Hardcoded URLs
                The {% url %} Template Tag
                Using get_absolute_url for Redirects
        11. A Simple Form
            Moving Validation Logic into a Form
                Exploring the Forms API with a Unit Test
                Switching to a Django ModelForm
                Testing and Customising Form Validation
            Using the Form in Our Views
                Using the Form in a View with a GET Request
                A Big Find and Replace
            Using the Form in a View That Takes POST Requests
                Adapting the Unit Tests for the new_list View
                Using the Form in the View
                Using the Form to Display Errors in the Template
            Using the Form in the Other View
                A Helper Method for Several Short Tests
            Using the Form’s Own Save Method
        12. More Advanced Forms
            Another FT for Duplicate Items
                Preventing Duplicates at the Model Layer
                A Little Digression on Queryset Ordering and String Representations
                Rewriting the Old Model Test
                Some Integrity Errors Do Show Up on Save
            Experimenting with Duplicate Item Validation at the Views Layer
            A More Complex Form to Handle Uniqueness Validation
            Using the Existing List Item Form in the List View
        13. Dipping Our Toes, Very Tentatively, into JavaScript
            Starting with an FT
            Setting Up a Basic JavaScript Test Runner
            Using jQuery and the Fixtures Div
            Building a JavaScript Unit Test for Our Desired Functionality
            Javascript Testing in the TDD Cycle
            Columbo Says: Onload Boilerplate and Namespacing
            A Few Things That Didn’t Make It
        14. Deploying Our New Code
            Staging Deploy
            Live Deploy
            What to Do If You See a Database Error
            Wrap-Up: git tag the New Release
    III. More Advanced Topics
        15. User Authentication, Integrating Third-Party Plugins, and Mocking with JavaScript
            Mozilla Persona (BrowserID)
            Exploratory Coding, aka "Spiking"
                Starting a Branch for the Spike
                Frontend and JavaScript Code
                The Browser-ID Protocol
                The Server Side: Custom Authentication
            De-spiking
                A Common Selenium Technique: Explicit Waits
                Reverting Our Spiked Code
            JavaScript Unit Tests Involving External Components: Our First Mocks!
                Housekeeping: A Site-Wide Static Files Folder
                Mocking: Who, Why, What?
                Namespacing
                A Simple Mock to Unit Tests Our initialize Function
                More Advanced Mocking
                Checking Call Arguments
                QUnit setup and teardown, Testing Ajax
                More Nested Callbacks! Testing Asynchronous Code
        16. Server-Side Authentication and Mocking in Python
            A Look at Our Spiked Login View
            Mocking in Python
                Testing Our View by Mocking Out authenticate
                Checking the View Actually Logs the User In
            De-spiking Our Custom Authentication Backend: Mocking Out an Internet Request
                1 if = 1 More Test
                Patching at the Class Level
                Beware of Mocks in Boolean Comparisons
                Creating a User if Necessary
                The get_user Method
            A Minimal Custom User Model
                A Slight Disappointment
                Tests as Documentation
                Users Are Authenticated
            The Moment of Truth: Will the FT Pass?
            Finishing Off Our FT, Testing Logout
        17. Test Fixtures, Logging, and Server-Side Debugging
            Skipping the Login Process by Pre-creating a Session
                Checking It Works
            The Proof Is in the Pudding: Using Staging to Catch Final Bugs
                Setting Up Logging
                Fixing the Persona Bug
            Managing the Test Database on Staging
                A Django Management Command to Create Sessions
                Getting the FT to Run the Management Command on the Server
                An Additional Hop via subprocess
            Baking In Our Logging Code
                Using Hierarchical Logging Config
            Wrap-Up
        18. Finishing "My Lists": Outside-In TDD
            The Alternative: "Inside Out"
            Why Prefer "Outside-In"?
            The FT for "My Lists"
            The Outside Layer: Presentation and Templates
            Moving Down One Layer to View Functions (the Controller)
            Another Pass, Outside-In
                A Quick Restructure of the Template Inheritance Hierarchy
                Designing Our API Using the Template
                Moving Down to the Next Layer: What the View Passes to the Template
            The Next "Requirement" from the Views Layer: New Lists Should Record Owner
                A Decision Point: Whether to Proceed to the Next Layer with a Failing Test
            Moving Down to the Model Layer
                Final Step: Feeding Through the .name API from the Template
        19. Test Isolation, and "Listening to Your Tests"
            Revisiting Our Decision Point: The Views Layer Depends on Unwritten Models Code
            A First Attempt at Using Mocks for Isolation
                Using Mock side_effects to Check the Sequence of Events
            Listen to Your Tests: Ugly Tests Signal a Need to Refactor
            Rewriting Our Tests for the View to Be Fully Isolated
                Keep the Old Integrated Test Suite Around as a Sanity Check
                A New Test Suite with Full Isolation
                Thinking in Terms of Collaborators
            Moving Down to the Forms Layer
                Keep Listening to Your Tests: Removing ORM Code from Our Application
            Finally, Moving Down to the Models Layer
                Back to Views
            The Moment of Truth (and the Risks of Mocking)
            Thinking of Interactions Between Layers as "Contracts"
                Identifying Implicit Contracts
                Fixing the Oversight
            One More Test
            Tidy Up: What to Keep from Our Integrated Test Suite
                Removing Redundant Code at the Forms Layer
                Removing the Old Implementation of the View
                Removing Redundant Code at the Forms Layer
            Conclusions: When to Write Isolated Versus Integrated Tests
                Let Complexity Be Your Guide
                Should You Do Both?
                Onwards!
        20. Continuous Integration (CI)
            Installing Jenkins
                Configuring Jenkins Security
                Adding Required Plugins
            Setting Up Our Project
            First Build!
            Setting Up a Virtual Display so the FTs Can Run Headless
            Taking Screenshots
            A Common Selenium Problem: Race Conditions
            Running Our QUnit JavaScript Tests in Jenkins with PhantomJS
                Installing node
                Adding the Build Steps to Jenkins
            More Things to Do with a CI Server
        21. The Token Social Bit, the Page Pattern, and an Exercise for the Reader
            An FT with Multiple Users, and addCleanup
            Implementing the Selenium Interact/Wait Pattern
            The Page Pattern
            Extend the FT to a Second User, and the "My Lists" Page
            An Exercise for the Reader
        22. Fast Tests, Slow Tests, and Hot Lava
            Thesis: Unit Tests Are Superfast and Good Besides That
                Faster Tests Mean Faster Development
                The Holy Flow State
                Slow Tests Don’t Get Run as Often, Which Causes Bad Code
                We’re Fine Now, but Integrated Tests Get Slower Over Time
                Don’t Take It from Me
                And Unit Tests Drive Good Design
            The Problems with "Pure" Unit Tests
                Isolated Tests Can Be Harder to Read and Write
                Isolated Tests Don’t Automatically Test Integration
                Unit Tests Seldom Catch Unexpected Bugs
                Mocky Tests Can Become Closely Tied to Implementation
                But All These Problems Can Be Overcome
            Synthesis: What Do We Want from Our Tests, Anyway?
                Correctness
                Clean, Maintainable Code
                Productive Workflow
                Evaluate Your Tests Against the Benefits You Want from Them
            Architectural Solutions
                Ports and Adapters/Hexagonal/Clean Architecture
                Functional Core, Imperative Shell
            Conclusion
        Obey the Testing Goat!
            Testing Is Hard
                Keep Your CI Builds Green
                Take Pride in Your Tests, as You Do in Your Code
            Remember to Tip the Bar Staff
            Don’t Be a Stranger!
        A. PythonAnywhere
            Starting a virtualenv
            Running Firefox Selenium Sessions with Xvfb
            Setting Up Django as a PythonAnywhere Web App
            Cleaning Up /tmp
            Screenshots
            The Deployment Chapter
        B. Django Class-Based Views
            Class-Based Generic Views
            The Home Page as a FormView
            Using form_valid to Customise a CreateView
            A More Complex View to Handle Both Viewing and Adding to a List
                The Tests Guide Us, for a While
                Until We’re Left with Trial and Error
                Back on Track
                Is That Your Final Answer?
            Compare Old and New
            Best Practices for Unit Testing CBGVs?
                Take-Home: Having Multiple, Isolated View Tests with Single Assertions Helps
        C. Provisioning with Ansible
            Installing System Packages and Nginx
            Configuring Gunicorn, and Using Handlers to Restart Services
            What to Do Next
                Move Deployment out of Fabric and into Ansible
                Use Vagrant to Spin Up a Local VM
        D. Testing Database Migrations
            An Attempted Deploy to Staging
            Running a Test Migration Locally
                Entering Problematic Data
                Copying Test Data from the Live Site
                Confirming the Error
            Inserting a Data Migration
                Re-creating the Old Migration
            Testing the New Migrations Together
            Conclusions
        E. Behaviour-Driven Development (BDD)
            What is BDD?
            Basic Housekeeping
            Writing an FT as a "Feature" using Gherkin Syntax
                As-a /I want to/So that
                Given/When/Then
                Not Always A Perfect Fit!
            Coding the Step Functions
                Generating Placeholder Steps
            First Step Definition
            setUp and tearDown Equivalents in environment.py
            Another run
            Capturing Parameters in Steps
            Comparing the Inline-Style FT
            BDD Encourages Structured Test Code
            The Page Pattern as an Alternative
            BDD Might Be Less Expressive than Inline Comments
            Will Nonprogrammers Write Tests?
            Some Tentative Conclusions
        F. Cheat Sheet
            Initial Project Setup
            The Basic TDD Workflow
            Moving Beyond dev-only Testing
            General Testing Best Practices
            Selenium/Functional Testing Best Practices
            Outside-In, Test Isolation Versus Integrated Tests, and Mocking
        G. What to Do Next
            Notifications—Both on the Site and by Email
            Switch to Postgres
            Run Your Tests Against Different Browsers
            404 and 500 Tests
            The Django Admin Site
            Write Some Security Tests
            Test for Graceful Degradation
            Caching and Performance Testing
            JavaScript MVC Frameworks
            Async and Websockets
            Switch to Using py.test
            Check out coverage.py
            Client-Side Encryption
            Your Suggestion Here
        H. Bibliography
    Index


## Preface

If you have any comments, questions, or suggestions, I’d love to hear from you. You can reach me directly via <obeythetestinggoat@gmail.com>, or on Twitter @hjwp. You can also check out the website and my blog, and there’s a mailing list.



## Aims of This Book

My main aim is to impart a methodology—a way of doing web development, which I think makes for better web apps and happier developers. There’s not much point in a book that just covers material you could find by googling, so this book isn’t a guide to Python syntax, or a tutorial on web development per se. Instead, I hope to teach you how to use TDD to get more reliably to our shared, holy goal: clean code that works.

With that said: I will constantly refer to a real practical example, by building a web app from scratch using tools like Django, Selenium, jQuery, and Mock. I’m not assuming any prior knowledge of any of these, so you should come out of the other end of this book with a decent introduction to those tools, as well as the discipline of TDD.


## Outline

I’ve split this book into three parts.

Part I (Chapters 1–6): The basics
    Dives straight into building a simple web app using TDD. We start by writing a functional test (with Selenium), then we go through the basics of Django—models, views, templates—with rigorous unit testing at every stage. I also introduce the Testing Goat. 
Part II (Chapters 7–14): Web development essentials
    Covers some of the trickier but unavoidable aspects of web development, and shows how testing can help us with them: static files, deployment to production, form data validation, database migrations, and the dreaded JavaScript. 
Part III (Chapters 15–20): More advanced topics
    Mocking, integrating a third-party authentication system, Ajax, test fixtures, Outside-In TDD, and Continuous Integration (CI). 

We appreciate, but do not require, attribution. An attribution usually includes the title, author, publisher, and ISBN. For example: “Test-Driven Development with Python by Harry Percival (O’Reilly). Copyright 2014 Harry Percival, 978-1-449-36482-3.”


## Required Python Packages

Once you have pip installed, it’s trivial to install new Python packages. We’ll install some as we go, but there are a couple we’ll need right from the beginning, so you should install them right away:

    Django, sudo pip3 install django==1.8.4 (omit the sudo on Windows). This is our web framework. You should make sure you have version 1.8[2] installed and that you can access the django-admin.py executable from a command line. The Django documentation has some installation instructions if you need help.

    Selenium, sudo pip3 install --upgrade selenium (omit the sudo on Windows), a browser automation tool that we’ll use to drive what are called functional tests. Make sure you have the absolute latest version installed. Selenium is engaged in a permanent arms race with the major browsers, trying to keep up with the latest features. If you ever find Selenium misbehaving for some reason, the answer is often that it’s a new version of Firefox and you need to upgrade to the latest Selenium …


# Part I. The Basics of TDD and Django

In this first part, I’m going to introduce the basics of Test-Driven Development (TDD). We’ll build a real web application from scratch, writing tests first at every stage.

In this first part, I’m going to introduce the basics of Test-Driven Development (TDD). We’ll build a real web application from scratch, writing tests first at every stage.

We’ll cover functional testing with Selenium, as well as unit testing, and see the difference between the two. I’ll introduce the TDD workflow, what I call the unit-test/code cycle. We’ll also do some refactoring, and see how that fits with TDD. Since it’s absolutely essential to serious software engineering, I’ll also be using a version control system (Git). We’ll discuss how and when to do commits and integrate them with the TDD and web development workflow.

We’ll be using Django, the Python world’s most popular web framework (probably). I’ve tried to introduce the Django concepts slowly and one at a time, and provide lots of links to further reading. 


## Chapter 1. Getting Django Set Up Using a Functional Test

### Obey the Testing Goat! Do Nothing Until You Have a Test

In TDD the first step is always the same: write a test.

First we write the test, then we run it and check that it fails as expected. Only then do we go ahead and build some of our app. 

Make functional_tests.py

assure ourselves that we understand what it’s doing:

    Starting a Selenium webdriver to pop up a real Firefox browser window
    Using it to open up a web page which we’re expecting to be served from the local PC
    Checking (making a test assertion) that the page has the word "Django" in its title


For now though, we have a failing test, so that means we’re allowed to start building our app.


### Getting Django Up and Running

The first step in getting Django up and running is to create a project.

django-admin.py startproject superlists_project


######
 NOT FROM THE BOOK BUT FROM TASKBUSTER
######

Set up enviroment variables

http://www.marinamele.com/taskbuster-django-tutorial/settings-different-environments-version-control#django-security

cd $VIRTUAL_ENV/bin

 If you type ls you will see that it contains the files we just described. Edit the postactivate file and add the secret key line

export SECRET_KEY="your_secret_django_key"

Note: don’t put any spaces around the = sign.

Next edit the predeactivate file and add the line:

unset SECRET_KEY

This way, if you type:

$ workon tb_dev
$ echo $SECRET_KEY
your_secret_django_key
$ deactivate
$ echo $SECRET_KEY
-

Where the last line indicates that there is no output. This means that the variable SECRET_KEY  is only visible when working in this virtual environment, as we wanted.

Repeat the same process for the tb_test virtual environment.

And finally, edit the base.py file, remove the SECRET_KEY  and add the following lines:
    
from django.core.exceptions import ImproperlyConfigured
 
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
 
SECRET_KEY = get_env_variable('SECRET_KEY')

The function get_env_variable  tries to get the variable var_name  from the environment, and if it doesn’t find it, it raises an ImproperlyConfigured  error. This way, when you try to run your app and the SECRET_KEY  variable is not found, we will be able to see a message indicating why our project fails.

Let’s check that it all works as expected. Save the base.py, deactivate both environments and activate them again, in different terminal tabs.

Run the development server in the tb_dev environment

$ python manage.py runserver

and run the functional test in the tb_test environment

$ python functional_tests/all_users.py

Hope the test also works for you!!

Note: When deploying your app, you will have to specify the SECRET_KEY  in your server. For example, if you are using Heroku, you can use:
    
$ heroku config:set SECRET_KEY="your_secret_key"

But don’t worry, we’ll cover Heroku latter in this tutorial!! 


#####
 BACK TO TDD
#####

For now, the important thing to know is that the superlists/superlists folder is for stuff that applies to the whole project—like settings.py for example, which is used to store global configuration information for the site.

You’ll also have noticed manage.py. That’s Django’s Swiss Army knife, and one of the things it can do is run a development server. Let’s try that now. Do a cd superlists to go into the top-level superlists folder (we’ll work from this folder a lot) and then run:

$ python3 manage.py runserver

Leave that running, and open another command shell. In that, we can try running our test again (from the folder we started in):

$ python3 functional_tests.py


Well, it may not look like much, but that was our first ever passing test! Hooray!


### Starting a Git Repository

TDD goes hand in hand with version control, so I want to make sure I impart how it fits into the workflow.

From this point onwards, the top-level superlists folder will be our working directory. Whenever I show a command to type in, it will assume we’re in this directory. Similarly, if I mention a path to a file, it will be relative to this top-level directory. So superlists/settings.py means the settings.py inside the second-level superlists. Clear as mud? If in doubt, look for manage.py; you want to be in the same directory as manage.py.

Add and commit everything to git.











https://github.com/hjwp/book-example/