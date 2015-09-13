# fyndiq_assignment
Smart Url Shortener Django framework app that shortens the url provided with usage of a word list so that urls do not contain meaningless hashes but a related word in them.

  [example url: http://techcrunch.com/2012/12/28/pinterest-lawsuit/]
  
  [shortened url: http://mysite.com/lawsuit/]
  
# Setup
  If no virtual environment is set:
  
    pip install virtualenvwrapper
    
    mkvirtualenv django_project
    
    workon django_project

  Download the repository and Install Django or  use requirements.txt( pip install -r requirements.txt )
  
# Create cleaned data and load it to database(sqlite)
  Under the Resource folder "words.txt" file includes the original form of word list.
  
  Same folder also includes  "fixed_words.txt" as cleaned data. You can directly use this file to upload to DB.
  
  However, If one would like to create the cleaned data again, he/she could use the command:
  
    $ cd Resource
    
    $ cat words.txt | tr A-Z a-z | sed 's/[^a-zA-Z0-9]//g' > fixed_words.txt

  To load this created "fixed_words.txt" to DB a django command was registered as wordlist. Simply type:
  
    python manage.py wordlist
    
  Note that In the project, It should be ready. If you decide to use a brand new DB, then better follow above instruction.
  
  ! Do not forget to make migrations If a brand new DB is to be used.
  
    python manage.py migrate
    
# Run the App
  python manage.py runserver 0.0.0.0:8000

Good Luck..
  
