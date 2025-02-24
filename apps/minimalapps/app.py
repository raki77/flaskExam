from flask import Flask, render_template, url_for, current_app, g, request, redirect, flash
from email_validator import validate_email, EmailNotValidError

import logging
import os
from flask_debugtoolbar import DebugToolbarExtension

from flask_mail import Mail, Message

# 여기에서 호출하면 오류
# print(cu)

# flask 클래스를 인스턴스화
app = Flask(__name__) 

ctx = app.app_context()
ctx.push()

# print("current app : " , current_app)
# print("current app name : " , current_app.name)

app.config["SECRET_KEY"] = "1234567"
app.logger.setLevel(logging.DEBUG)

# 리다이렉트 중단하지 않도록 한다.
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Mail 클래스의 컨피그를 추가한다
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")





toolbar = DebugToolbarExtension(app)

# flask-mail 확장을 등록한다
mail = Mail(app)





@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        print("이메일 보냄")        
        
        username = request.form["username"]
        print("username:", username)
        
        email = request.form["email"]
        print("email:", email)
        
        description = request.form["description"]
        print("description:", description)
                
        # 입력 체크
        is_valid=True
        print("is_valid:", is_valid)
        if not username:
            flash("사용자명은 필수")
            is_valid=False
            
        if not email:
            flash("메일주소 필수")
            is_valid=False
        
        try:
            validate_email(email)
        except EmailNotValidError :
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid=False
            
        if not description:
            flash("문의내용 필수")
            is_valid=False
            
        if not is_valid:
            redirect(url_for("contact"))        
            
        # 메일을 보낸다
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )
        # 문의 완료 엔드포인트로 리다이렉트한다
        flash("문의 내용은 메일로 송신했습니다. 문의해 주셔서 감사합니다.")   
            
        # # contact 엔드포인트로 리다이렉트
        # flash("문의해 주셔서 감사.")    
        return redirect(url_for("contact_complete"))    
    return render_template("contact_complete.html")




def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


    
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
