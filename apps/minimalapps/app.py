from flask import Flask, render_template, url_for, current_app, g, request, redirect


# 여기에서 호출하면 오류
# print(cu)


# flask 클래스를 인스턴스화
app = Flask(__name__) 

ctx = app.app_context()
ctx.push()

print("current app : " , current_app)
print("current app name : " , current_app.name)



@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        print("이메일 보냄")
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")



    
@app.route('/', methods=["GET"])
def main():
    return render_template("index2.html")

@app.route('/hi')
def hi():
    return '<h1>hi</h1>'

@app.route('/hello/<name>', methods=["GET", "POST"])
def hello(name):
    return f'<h1>Hi, {name}</h1>'


@app.route('/hello/<int:num1>', methods=["GET", "POST"])
def calc(num1):
    result=num1+1
    return f'<h1>Hi, result : {result}</h1>'

@app.route('/showproduct/<product>', methods=["GET", "POST"])
def show_product(product):
    return render_template("index.html", product=product)

@app.route('/hello/world')
def helloworld():
    return '<h1>hello, World</h1>'

# @app.route('/hello/world2/<key>')
# def helloworld2(key):
#     return render_template("index.html", key=key)

##############################################################


# @app.route('/', methods=["GET", "POST"])
# def main():
#     return render_template("index2.html") 




# test용 함수, test_request_context 
# with app.test_request_context(): 
#     # /
#     print(url_for("index")) 
#     # /hello/world
#     print(url_for("helloworld")) 
#     # /hello/world/key
#     print(url_for("helloworld2", key="key"))
