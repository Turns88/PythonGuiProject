
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutProject Management Planning Techniques es academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10910115
#    Student name: Paul Turner
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Runners-Up
#
#  In this assignment you will combine your knowledge of HTMl
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to access online data.  See the
#  instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these functions
# only.  You can import other functions provided they are standard
# ones that come with the default Python/IDLE implementation and NOT
# functions from modules that need to be downloaded and installed
# separately.  Note that not all of the imported functions below are
# needed to successfully complete this assignment.

# The function for accessing a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# The function for displaying a web document in the host
# operating system's default web browser.  We have given
# the function a distinct name to distinguish it from the
# built-in "open" function for opening local files.
# (You WILL need to use this function in your solution.)
from webbrowser import open as urldisplay

# Import some standard Tkinter functions. (You WILL need to use
# some of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to open a local HTML file in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." address).  The file to be opened must be in the same
# folder as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

##### DEVELOP YOUR SOLUTION HERE #####
#create a window

runner_up_window = Tk()

runner_up_window.configure (bg = 'grey')

#Give the window a title

runner_up_window.title("Celebrating the one who always comes second!")




# create frame
title_frame = Frame(runner_up_window,  bg = 'grey')
title_frame.grid( row = 0, column = 0 ,sticky = N)

bottom_frame = Frame(runner_up_window,bg = 'grey')
bottom_frame.grid( row = 3, column = 0  )

top_frame = Frame(runner_up_window)
top_frame.grid( row = 1, column = 0, )

middle_frame = Frame(runner_up_window,  bg = 'grey')
middle_frame.grid(row = 2 , column = 0)




#Give the application a visible title
title_label = Label(title_frame, text = "Celebrating the one who always comes second!")

title_label.grid(row = 0 , column = 0,pady =  5 , sticky = W)
title_label.configure(font=("Arial", 30, "bold"))

#create a label to display the current runner up
runner_up_label = Label(bottom_frame, text = "THE RUNNER UP IS........")
runner_up_label.grid(row = 0, column = 0)

others_label = Label(bottom_frame, text = "OTHER COMPETITORS")
others_label.grid(row = 0 , column = 1)

#define global variables so that the runner up and other competitor data generated from each
#seperate  page function can be used in the save function to commit that data to the database.
runner_up_competitor = []
runner_up_property = [] 
others =[]


# define function that allows the user to save the current displayed list
def save():
    connection = connect(database = 'runners_up.db')

    # Get a cursor on the database.
    runners_up_db = connection.cursor()

    #clear the tables of all data before the next updating the database with new data
    runners_up_db.execute( 'DELETE FROM runner_up;')
    connection.commit()
    
    runners_up_db.execute ('DELETE FROM others;')
    connection.commit()

    # Execute an SQL query to update the database with the  data generated from each pages function
    sql_runner_up = 'INSERT INTO runner_up(competitor, property) VALUES (?,?);'
    val_runner_up = (runner_up_competitor, runner_up_property)

    
    
    
    runners_up_db.execute(sql_runner_up, val_runner_up)
    connection.commit()

    runners_up_db.executemany('INSERT INTO others(position, competitor, property) VALUES (?,?,?);',others,)
    connection.commit()


    # Close the cursor.
    runners_up_db.close()

    # Close the database connection.
    connection.close()
    

# Create a function that will clear both text boxes so a new list can be populated without duplication.

def clear_text():
    selected_list_runner_up.delete('1.0', 'end')
    selected_list.delete('1.0', 'end')
# Allow the program to work with the text widget in order to clear and display the generated lists.
def enable_input():
    selected_list.configure(state="normal")
    selected_list_runner_up.configure(state="normal")
#Allow the program to stop the user from  manipulating the data that appears in the text widgets.
def disable_input():
    selected_list.configure(state="disabled")
    selected_list_runner_up.configure(state="disabled")
    

#Create function to search through the non live list, select a runner up and display the other competitors
def city():
#Allow the function to use the text widget
    enable_input()
#clear any previous text from the text widget to prevent duplicates
    clear_text()
    
    city_text = open('Top_10_most_livable_cities_2019.html')

    city_contents = city_text.read()
#Replace the tied score for better readability 
    city_contents = city_contents.replace("T8", "8")

    city_contents = city_contents.replace("&#x27;", "'")
    city_contents = city_contents.replace("&#39;", "'")
    city_contents = city_contents.replace("&amp;", "&")
    
#Break the  information into 3 sections position,competitor and a property
#Use a different regular expression to target each section and assign the matches to variables
    
    city_rank = (findall (r'<h2>([A-Za-z\d]+)\. ',city_contents))
    city_name = (findall (r'<h2>[A-Z\d]+\.\s+([A-Za-z]+\,\s[A-Za-z]+)', city_contents))
    city_rating =(findall (r'<p><strong>Overall rating \(out of 100\):</strong> ([0-9]+\.[0-9]+)</p>', city_contents))

#Combine the 3 different variables into one list using the zip function
    city_combined = list(zip(city_rank, city_name, city_rating))

#remove the runner up from the other competitor list
    city_combined.remove(city_combined[8])
    
#Select the runner up's position from the generated lists
    
    city_rup = f"Rank {city_rank[8]} {city_name[8]} Overall Rating {city_rating[8]}"
    
#Declare and update the global variables, if the user clicks save it will trigger the save function
# and commit these values the database

    global runner_up_competitor
    runner_up_competitor = f"{city_name[8]}" 
    global runner_up_property
    runner_up_property = f"{city_rating[8]}"
    global others
    others = city_combined
#Populate the text widgets  with the runner up and other competitor information
    for (city_rank, city_name, city_rating) in city_combined:
        city_top_10 = f"Rank {city_rank}  {city_name} Overall Rating {city_rating}\n\n"
        selected_list.insert(END,city_top_10)


    selected_list_runner_up.insert(END, city_rup)


    city_text.close()
    disable_input()
 #disable input to the text box to prevent user manipulation   
    
def ny_books():
#Allow the function to use the text widget
    enable_input()
#clear any previous text from the text widget to prevent duplicates
    clear_text()
    
    
    ny_books_text = open('top_10_ny_times_books.html')

    ny_books_contents  = ny_books_text.read()
#find and replace any common html markup from the text to ensure robustness
    ny_books_contents = ny_books_contents.replace("&#x27;", "'")
    ny_books_contents = ny_books_contents.replace("&#39;", "'")
    ny_books_contents = ny_books_contents.replace("&amp;", "&")
    
#Break the  information into 3 sections position,competitor and a property
#Use a different regular expression to target each section and assign the matches to variables
    
    book_rank = (findall (r'<meta itemProp="position" content="([0-9]|[1][0])"/><meta', ny_books_contents))
    book_name = (findall (r'<h3 class="css-5pe77f" itemProp="name">([a-zA-Z0-9\'\"\;\:\,\s\\#\.(\)\-\&\!]*)<\/h3>', ny_books_contents))
    book_author =(findall (r'<p class="css-hjukut" itemProp="author">([a-zA-Z0-9\'\"\;\:\,\s\\#\.(\)\-\&\!]*)<\/p>',ny_books_contents))

#Combine the 3 different variables into one list using the zip function
    
    ny_books_combined = list(zip(book_rank, book_name, book_author))
    
#remove the runner up from the other competitor list
    
    ny_books_combined.remove(ny_books_combined[1])

    ny_books_rup = f"Rank {book_rank[1]} Title {book_name[1]} Authored {book_author[1]}"
    
#Declare and update the global variables, if the user clicks save it will trigger the save function
# and commit these values the database   

    global others
    others = ny_books_combined

    global runner_up_competitor
    runner_up_competitor = f"{book_name[1]}"
    
    global runner_up_property
    runner_up_property = f"{book_author[1]}"

#Populate the text widgets  with the runner up and other competitor information
    for (book_rank, book_name, book_author) in ny_books_combined:
        ny_books_top_10 = f"Rank {book_rank} Title {book_name} Authored {book_author}\n\n"
        selected_list.insert(END,ny_books_top_10)

    
    selected_list_runner_up.insert(END,ny_books_rup)

    
    ny_books_text.close()
    
#disable input to the text box to prevent user manipulation
    
    disable_input()
    
def ios_apps():
#Allow the function to use the text widget
    enable_input()
#clear any previous text from the text widget to prevent duplicates
    clear_text()
    
    
    ios_text =  open( 'top_10_ios_apps.html')

    ios_contents = ios_text.read()
#find and replace any html markup from the text
    ios_contents = ios_contents.replace("&#39;", "'")
    ios_contents = ios_contents.replace("&#x27;", "'")
    ios_contents = ios_contents.replace("&amp;", "&")
    
#Break the  information into 3 sections position,competitor and a property
#Use a different regular expression to target each section and assign the matches to variables
    
    app_rank = (findall (r'td class="info top-free-rank" >([0-9]|10)</td>',ios_contents))
    app_name = (findall (r'href="/app-sales-data/[0-9]+/[a-zA-Z0-9\'\"\;\:\,\s\\#\.(\)\-\&\!]*/">([a-zA-Z0-9\'\"\;\:\,\s\\#\.(\)\-\&\!]*)</a>', ios_contents))
    app_developer =(findall (r'data/publisher/[0-9]+/[a-zA-Z0-9\'\"\;\:\,\s\\#\.(\)\-\&\!]*/">([a-zA-Z0-9\'\"\;\:\,\s\\#\.(\)\-\&\!]*)</a>', ios_contents))
    

    ios_combined = list(zip(app_rank, app_name, app_developer))
#remove the runner up from the other competitor list
    ios_combined.remove(ios_combined[1])
    
    app_rup = f"Rank {app_rank[1]} Title {app_name[1]} Developed By {app_developer[1]}"
    
#Declare and update the global variables, if the user clicks save it will trigger the save function
# and commit these values the database

    global runner_up_competitor
    runner_up_competitor = f"{app_name[1]}" 
    global runner_up_property
    runner_up_property = f"{app_developer[1]}"
    global others
    others = ios_combined
#Populate the text widgets  with the runner up and other competitor information
    for (app_rank, app_name, app_developer) in ios_combined:
        ios_top_10 = f"Rank {app_rank} Title {app_name} Developed By {app_developer}\n\n"
        selected_list.insert(END,ios_top_10)
        
    selected_list_runner_up.insert(END,app_rup)

    ios_text.close()

#disable input to the text box to prevent user manipulation
    disable_input()
    
#Create a function                        

def aria_singles():
#Allow the function to use the text widget
    enable_input()
    clear_text()
    
   
    aria_text = open('top_10_singles.html')


    aria_contents = aria_text.read()
#find and replace any html markup from the text
    aria_contents = aria_contents.replace("&amp;", "&")
    aria_contents = aria_contents.replace("&#x27;", "'")
    aria_contents = aria_contents.replace("&#39;", "'")
    

#Break the  information into 3 sections position,competitor and a property
#Use a different regular expression to target each section and assign the matches to variables
    
    aria_ranks= (findall (r'<div class="c-chart-item__rank">\n\s+\<span>([0-9]|10)</span>', aria_contents))
    aria_artist =(findall(r'<a class="c-chart-item__artist">([a-zA-Z0-9\'\"\;\:\,\s\\#\.(\)\-\&\!]*)</a>', aria_contents))
    aria_song_name = (findall(r'<a class="c-chart-item__title">([a-zA-Z0-9\'\"\;\:\,\s\\#\.(\)\-\&\!]*)</a>',  aria_contents))

    combined = list(zip(aria_ranks, aria_artist, aria_song_name))
#remove the runner up from the other competitor list
    combined.remove(combined[1])
    
    rup = f"Rank {aria_ranks[1]} Title {aria_song_name[1]} Artist {aria_artist[1]}"
    
#Declare and update the global variables, if the user clicks save it will trigger the save function
# and commit these values the database

    global runner_up_competitor
    runner_up_competitor = f"{aria_song_name[1]}" 
    global runner_up_property
    runner_up_property = f"{aria_artist[1]}"
    global others
    others = combined
    
#Populate the text widgets  with the runner up and other competitor information    
    for (aria_ranks, aria_artist, aria_song_name) in combined:
        aria_top_10 = f"Rank {aria_ranks} Title {aria_song_name} Artist {aria_artist}\n\n"
        selected_list.insert(END,aria_top_10)
        
    selected_list_runner_up.insert(END,rup)


    aria_text.close()
#disable input to the text box to prevent user manipulation
    disable_input()
    
#Create a function that takes user input from the menu  button downloads the required page and triggers the
#function that commences the search of the designated website using  regular expressions.

def initialize_choice ():
    
    user_selection = what_option.get()
    if user_selection == 'Not Live: 2019 Top 10 Most Liveable Cities In The World':
        
        city()
        
    elif user_selection == 'Live: Aria Charts Top 10 Current Singles':
        download( url = 'https://www.aria.com.au/charts/singles-chart',
                  target_filename = 'top_10_singles')
        
        aria_singles()

    elif user_selection == 'Live: Top 10 Current IOS Apps' :
        download( url = 'https://thinkgaming.com/app-sales-data/top-free-games/',
                                    target_filename = 'top_10_ios_apps')
        ios_apps()
        
    elif user_selection == 'Live: Top 10 NY Times Monthly Best Selling Mass Market Books':
        download( url = 'https://www.nytimes.com/books/best-sellers/mass-market-monthly/',
                                    target_filename = 'top_10_ny_times_books')
        ny_books()
        
#Define a function for  downloading and opening webpage once the source button has  been pressed.


def select_web_page():
    user_selection = what_option.get()

    if user_selection == 'Not Live: 2019 Top 10 Most Liveable Cities In The World':
        open_html_file('/Users/paulturner/Documents/IFB104/Assignment 2a/Top_10_most_livable_cities_2019.html')
    elif user_selection == 'Live: Aria Charts Top 10 Current Singles':
        download( url = 'https://www.aria.com.au/charts/singles-chart',
                                    target_filename = 'top_10_singles')
        open_html_file('/Users/paulturner/Documents/IFB104/Assignment 2a/top_10_singles.html')
    elif user_selection =='Live: Top 10 Current IOS Apps':
        download( url = 'https://thinkgaming.com/app-sales-data/top-free-games/',
                                    target_filename = 'top_10_ios_apps')
        open_html_file('/Users/paulturner/Documents/IFB104/Assignment 2a/top_10_ios_apps.html')
    elif user_selection == 'Live: Top 10 NY Times Monthly Best Selling Mass Market Books':
        download( url = 'https://www.nytimes.com/books/best-sellers/mass-market-monthly/',
                                    target_filename = 'top_10_ny_times_books')
        open_html_file('/Users/paulturner/Documents/IFB104/Assignment 2a/top_10_ny_times_books.html')
        




#Create and position the background image of an unlucky runner-up!
road_runner = PhotoImage( file = "road_runner3.gif")

background_image = Label(top_frame, image = road_runner )

background_image.grid(row = 0, column = 0,pady= 5, sticky = W)


#Create the menu button to allow the user to pick which list they want to view

#The lists available to the user
option_list = [
    'Not Live: 2019 Top 10 Most Liveable Cities In The World' ,
    'Live: Aria Charts Top 10 Current Singles',
    'Live: Top 10 Current IOS Apps',
    'Live: Top 10 NY Times Monthly Best Selling Mass Market Books']

what_option = StringVar()
what_option.set( 'Choose a list to see who the runner up is!')
list_select_menu = OptionMenu(middle_frame, what_option, *option_list)
list_select_menu.grid(row =0, column = 0, padx = 20)
list_select_menu.configure(font=("Arial", 15, "italic"))


# create update button
update_button = Button(middle_frame,command = initialize_choice, text = "Update" , height = '3', width = '15', relief = 'ridge')
update_button.grid(row = 0 , column =1, padx = 20, pady = 10)

# create source button
source_button = Button(middle_frame, command = select_web_page, text = "Source", height = '3', width = '15', relief = 'raised')
source_button.grid(row = 0, column = 2, padx = 20, pady = 10)

#create a save button
save_button = Button(middle_frame, command = save, text = 'Save' , height = '3', width = '15', relief = 'sunken')
save_button.grid (row = 0, column =3, padx =  20, pady = 10)


#create a text box to  display the others list
selected_list = Text (bottom_frame,width = 65, bg  ='tan', state="disabled")
selected_list.grid(row = 1, column = 1, padx = 10, pady = 10)

#create a text box to display the runner up
selected_list_runner_up = Text (bottom_frame, width = 65, bg = 'tan',state="disabled" )
selected_list_runner_up.grid(row = 1, column = 0, padx = 10, pady = 10)

selected_list_runner_up.configure(font=("Arial", 13))
selected_list.configure(font=("Arial", 13))






#program
runner_up_window.mainloop()

    


