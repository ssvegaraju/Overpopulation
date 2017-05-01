#!C:\Users\ssveg\AppData\Local\Programs\Python\Python36-32\python.exe
"""Flask_SOLUZION_Client_Server.py

Based on
Text_SOLUZION_Client.py
 This file implements a simple "SOLUZION" client and server that
 permits a user ("problem solver") to explore a search tree
 for a suitably-formulated problem.  The user only has to
 input single-character commands to control the search.
 Output is both textual and graphical,
 consisting of some limited content sent to a browser
 via HTTP ("Ajax" but using JSON or other data rather than XML).

 The program is started by typing
 $ ../Flask-SOLZ-Client-and-Server.py Missionaries
(You can replace "Missionaries" with the name of your problem template.)

 The client is a browser window or tab, going to the URL:
 http://localhost:5000

 These things can be changed if needed by editing the code.

"""

DEBUG = False

import sys, os, importlib.util
sys.path.append(os.getcwd())

# Get the PROBLEM name from the command-line arguments

if len(sys.argv)<2:
  print('''
       Usage: 
Flask_SOLUZION_Client_Server.py <PROBLEM NAME>
       For example:
Flask_SOLUZION_Client_Server.py Missionaries
  ''')
  exit(1)
  
problem_name = sys.argv[1]
print("problem_name = "+problem_name)

try:
  spec = importlib.util.spec_from_file_location(problem_name, problem_name+".py")
  PROBLEM = spec.loader.load_module()
  spec.loader.exec_module(PROBLEM)
except Exception as e:
  print(e)
  exit(1)
  
THE_DIR = problem_name # Used in routing, if the vis code loads any image files.

from flask import Flask,  render_template, request, jsonify, safe_join, send_from_directory

NEW_SESSION = True
APPLICABILITY_VECTOR = None
STATE_IMAGE = ''
STATE_SVG = ''

# Initialize the Flask application
app = Flask(__name__)

if PROBLEM.BRIFL_SVG:
    PROBLEM.use_BRIFL_SVG()
    print("Using BRIFL SVG.")
    
# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')

# Route that will process the AJAX request,
# process the command, and return the resulting
# new state  as a proper JSON response (Content-Type, etc.)

@app.route('/_command')
def command():
    global STEP, DEPTH, OPERATORS, CURRENT_STATE, STATE_STACK
    global OK_OPS_STRING, NEW_SESSION, STATE_SVG
    command = request.args.get('command', 0, type=str)
    if DEBUG: print("Command received: "+str(command))
    if command=="start":
        initialize()
        try: 
           if PROBLEM.BRIFL_SVG:
            STATE_SVG = PROBLEM.render_state(CURRENT_STATE)
            if DEBUG: print("A new state graphic was produced.")
        except Exception as e:
           print("There was an exception when trying to do SVG rendering of the CURRENT_STATE.")
           print(e)
        return mes("You may begin solving the problem by choosing an operator to apply.", start=True)

    if DEBUG:
        print("\nStep "+str(STEP)+", Depth "+str(DEPTH))
        print("CURRENT_STATE = "+str(CURRENT_STATE))

    if command=="B" or command=="b": 
      if len(STATE_STACK)>1:
        STATE_STACK.pop()
        DEPTH -= 1
        STEP += 1
      else:
        if DEBUG: print("You're already back at the initial state.")
        return mes("You're already back at the initial state.")
      CURRENT_STATE = STATE_STACK[-1]
      update_applicability_vector(CURRENT_STATE)
      try: 
        if PROBLEM.BRIFL_SVG:
            STATE_SVG = PROBLEM.render_state(CURRENT_STATE)
            if DEBUG: print("A new state graphic was produced.")
      except Exception as e:
         print("There was an exception when trying to do SVG rendering of the CURRENT_STATE.")
         print(e)
      return mes("Backtracked.")
  
    if command=="H" or command=="h": return mes(show_instructions())
    if command=="Q" or command=="q": return mes("To quit, close the browser tab or window.")
    if command=="":
       if NEW_SESSION:
           return mes("Here is the starting state of the problem.")
       else:
           return mes("You didn't enter any command.")
    NEW_SESSION = False
    try:
      i = int(command)
    except:
      if DEBUG: print("Unknown command or bad operator number.")
      return mes("Unknown command or bad operator number.")
    if DEBUG: print("Operator "+str(i)+" selected.")
    if i<0 or i>= len(OPERATORS):
      if DEBUG: print("There is no operator with number "+str(i))
      return mes("There is no operator with number.")
    if APPLICABILITY_VECTOR[i]:
       CURRENT_STATE = OPERATORS[i].apply(CURRENT_STATE)
       STATE_STACK.append(CURRENT_STATE)
       DEPTH += 1
       STEP += 1
       update_applicability_vector(CURRENT_STATE)
       #print("APPLICABILITY_VECTOR = "+str(APPLICABILITY_VECTOR))
       if DEBUG: print(OK_OPS_STRING)
       try: 
         if PROBLEM.BRIFL_SVG:
             STATE_SVG = PROBLEM.render_state(CURRENT_STATE)
             if DEBUG: print("A new state graphic was produced.")
       except Exception as e:
         print("There was an exception when trying to do SVG rendering of the CURRENT_STATE.")
         print(e)

       if PROBLEM.goal_test(CURRENT_STATE): return(handle_win())
         
       return mes("Your selected action was taken. Now make your next move.")
    else:
       if DEBUG: print("Operator "+str(i)+" is not applicable to the current state.")
       return mes("Operator "+str(i)+" is not applicable to the current state.")
    if DEBUG: print("Operator "+command+" not yet supported.")
    return mes("Operator "+command+" not yet supported.")

def initialize():
  global STEP, DEPTH, OPERATORS, CURRENT_STATE, STATE_STACK, NEW_SESSION
  CURRENT_STATE = PROBLEM.copy_state(PROBLEM.INITIAL_STATE)  
  NEW_SESSION = True
  STATE_STACK = [CURRENT_STATE]
  STEP = 0
  DEPTH = 0
  update_applicability_vector(CURRENT_STATE) 
  try: 
     if PROBLEM.BRIFL_SVG: STATE_SVG = PROBLEM.render_state(CURRENT_STATE)
  except Exception as e:
     print("There was an exception when trying to do SVG rendering of the CURRENT_STATE.")
     print(e)
 
def mes(the_mess, start=False):
    global CURRENT_STATE, OK_OPS_STRING, STEP, DEPTH, STATE_IMAGE, STATE_SVG
    if start:
        return jsonify(
                   problem_title = PROBLEM.PROBLEM_NAME + ", version "+PROBLEM.PROBLEM_VERSION,
                   problem_desc = PROBLEM.PROBLEM_DESC,
                   problem_author = PROBLEM.PROBLEM_AUTHORS,
                   problem_creation_date = PROBLEM.PROBLEM_CREATION_DATE,
                   message=the_mess,
                   available_ops=OK_OPS_STRING,
                   current_state=str(CURRENT_STATE),
                   stats = "STEP = "+str(STEP)+"; DEPTH = "+str(DEPTH),
                   state_svg = STATE_SVG)

    else:
        return jsonify(message=the_mess,
                   available_ops=OK_OPS_STRING,
                   current_state=str(CURRENT_STATE),
                   stats = "STEP = "+str(STEP)+"; DEPTH = "+str(DEPTH),
                   state_svg = STATE_SVG)

@app.route('/get_image/<filename>')
def get_image(filename):
  global THE_DIR
#  safe_filename = safe_join(THE_DIR, filename)
  return send_from_directory(THE_DIR, filename, mimetype='image/jpg')  

  
OPERATORS=PROBLEM.OPERATORS
STATE_STACK = []
TITLE="Flask_SOLZ_Client_Server (Version 0-3)"

def mainloop():
  print(TITLE)
  print(PROBLEM.PROBLEM_NAME+"; "+PROBLEM.PROBLEM_VERSION)

def update_applicability_vector(s):
    global OPERATORS, APPLICABILITY_VECTOR, OK_OPS_STRING
    #print("OPERATORS: "+str(OPERATORS))
    APPLICABILITY_VECTOR = [op.is_applicable(s) for op in OPERATORS]  
    OK_OPS_STRING = ''
    for i in range(len(OPERATORS)):
      if APPLICABILITY_VECTOR[i]:
        OK_OPS_STRING += '<span class="OK_OPS">'+str(i)+": "+OPERATORS[i].name + "</span><br>\n"
    #OK_OPS_STRING += "<br>&nbsp;<br>Enter command: 0, 1, 2, etc. for operator; B-back; H-help; Q-quit."

def exit_client():
  print("Terminating Flask_SOLZ_Client_Server session.")
  log("Exiting")
  exit()

def handle_win():
  win_mes = '''CONGRATULATIONS!
You have solved the problem by reaching a goal state.

'''
  print(win_mes)
  return mes(win_mes)
  
#Do you wish to continue exploring?
#      answer = input("Y or N? >> ")
#      if answer=="Y" or answer=="y": print("OK, continue")
#      else: return

def show_instructions():
  return '''\nINSTRUCTIONS:\n
The current state of your problem session represents where you
are in the problem-solving process.  You can try to progress
forward by applying an operator to change the state.
To do this, click on the description of one of the applicable operators.
The program shows you a list of what operators are 
applicable in the current state.

You can also go backwards (undoing a previous step)
by typing 'B'.  

If you reach a goal state, you have solved the problem,
and the computer will usually tell you that, but it depends
on what kind of problem you are solving.'''

def apply_one_op():
    """Populate a popup menu with the names of currently applicable
       operators, and let the user choose which one to apply."""
    currently_applicable_ops = applicable_ops(CURRENT_STATE)
    #print "Applicable operators: ",\
    #    map(lambda o: o.name, currently_applicable_ops)
    print("Now need to apply the op")
    

def applicable_ops(s):
    """Returns the subset of OPERATORS whose preconditions are
       satisfied by the state s."""
    return [o for o in OPERATORS if o.is_applicable(s)]

# The following is only executed if this module is being run as the main
# program, rather than imported from another one.
if __name__ == '__main__':
  initialize()
  app.run()
  



 
