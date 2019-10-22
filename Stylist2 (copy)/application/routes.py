from flask import Flask, render_template, url_for, redirect, request
from application import app, db, bcrypt
from application.models import Users, Shoppinglist
from application.forms import  RegisterForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from application import login_manager

@app.route("/")
@app.route('/home')
def home():
  return render_template('home.html', title='Home')

@app.route("/about")
def about():
	return render_template ('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
      return redirect(url_for('home'))
  form = RegisterForm()
  if form.validate_on_submit():
    hashed_pw = bcrypt.generate_password_hash(form.password.data)
    user = Users(first_name=form.first_name.data, last_name=form.last_name.data,email=form.email.data, password=hashed_pw)
    db.session.add(user)                                                
    db.session.commit()
    return redirect(url_for('newitem'))
  return render_template ('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('home'))
  form = LoginForm()  
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      if next_page:
        return redirect(next_page)
      else:
        return redirect(url_for('lists'))
  return render_template('login.html', title='Login', form=form)
  
@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data
    current_user.email = form.email.data
    db.session.commit()
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.email.data = current_user.email
  return render_template('account.html', title='Account', form=form)

@app.route('/deleteaccount', methods=['POST'])
@login_required
def deleteaccount(current_user): 
  account_to_delete = Users.query.filter_by(current_user=users.id).first()
  db.session.delete(account_to_delete)
  db.session.commit()
  return redirect(url_for('home'))
  #return render_template('deleteaccount.html', delete=account_to_delete, form=form)

@app.route('/newitem')
@login_required
def newitem():
  return render_template('newitem.html', title='Add New Item')

#bought and not bought allows for the shoppling list able to be queried and return items where bought is either False or True. 
@app.route('/lists')
@login_required
def lists():
 if current_user.is_authenticated:
  bought = Shoppinglist.query.filter_by(creator=current_user, bought=True).all()
  notbought = Shoppinglist.query.filter_by(creator=current_user, bought=False).all()
  return render_template('lists.html', title='Lists', bought=bought, notbought=notbought, creator=current_user)

@app.route('/add', methods=['POST'])
def add():
  tobuy = Shoppinglist(text=request.form['shoppinglistitem'], creator=current_user, bought=False)
  db.session.add(tobuy)
  db.session.commit()
  return redirect(url_for('lists'))

#Bought route allows for items that have been added to the database to return specific items
@app.route('/bought/<id>')
def bought(id):
  tobuy = Shoppinglist.query.filter_by(id=int(id)).first()
  tobuy.bought = True
  db.session.commit()
  return redirect(url_for('lists'))


@app.route('/delete/<id>')
def delete(id):
  todelete = Shoppinglist.query.filter_by(id=int(id)).first()
  db.session.delete(todelete)
  db.session.commit()
  return redirect(url_for('lists'))

