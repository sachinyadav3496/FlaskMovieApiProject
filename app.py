from flask import Flask,render_template

app = Flask(__name__)  #__name__ --> Flask_Project

#pip install flask --> to install flask package

#app = Flask(__name__)
#__name__?? --> __main__

#domain --> page
#paths --> html page
@app.route("/")  #route --> decorator(path)
def index():     #/ --> domain --> localhost
    #return "hello world"
    return render_template("one.html")  #render_template(name of html page after templates folder)

#html page --> templates/one.html
#html page --> templates/html_pages/one.html --> render_template("html_pages/one.html")
 
@app.route("/home/")   #client --> localhost/home/
def home():
    return "<h1 style='color:red'>This is my first project</h1>"

#/home/simran -->Welcome simran
#/home/nitin --> Welcome Nitin
#/home/gaurav --> Welcome gaurav

@app.route("/home/<name>/")    #<name> --> name = variable #default type --> string
def showname(name):            #<int:age> --> age = variable (integer) #<float:f> --> float
    #return f"<h1 style='color:red'>Welcome {name} with age {age}</h1>"
    return render_template("one.html",n=name)  #n = key, name = value

#leftside--> name-->key and rightside --> name--> value


#browser --> localhost/simran/43/44/32
#    Per<40 --> F
#40<=per<50 --> D
#50<=per<60 --> B
#60-70 --> B+
#70-85 --> A
#85-100 --> A+
#return a string  --> Simran you got grade B

#pip install pymysql (powershell)
@app.route("/<name>/<int:m1>/<int:m2>/<int:m3>")
def marks(name,m1,m2,m3):
    """per = (m1+m2+m3)/3
    if per<40:
        return f"{name} has grade F"
    elif 40<per<50:
        return f"{name} has grade D"
    elif 50<=per<60:
        return f"{name} has grade B"
    elif 60<=per<70:
        return f"{name} has grade B+"
    elif 70<=per<85:
        return f"{name} has grade A"
    elif per>85:
        return f"{name} has grade A+"
    """
    data = {
        "name" : name,
        "maths" : m1,
        "science" : m2,
        "english" : m3
    }
    return render_template("one.html",d=data)


#jinja language --> Dynamic html pages
#jinja --> templating engine python
#jinja --> {{}}
#python file --> name="simran", html file --> {{name}}
"""if else --> {% if condition %}
                content
                {% endif %}
    if-elif-else ---> {% if condition %}
                        <h1> This is my first page</h1>
                      {% elif condition %}
                        content
                      {% else %}
                        content
                      {% endif %}   
    for --> {% for i in range(10) %}
                content
            {% endfor %}"""

app.run(host="localhost",port=80,debug=True)
#debug = True --> Show error on front page

