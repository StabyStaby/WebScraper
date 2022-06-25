import sqlite3
from flask import Blueprint, jsonify, render_template, request,flash, url_for,redirect
from website.scrape import scrapeName,scrapeForLastDate
from . import db
import json
from .models import User,Manga
from website.scrape import scrapeName,scrapeManga

views = Blueprint('views',__name__)

@views.route('/user',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('user')
        discordId = request.form.get('discordId')
        webhook = request.form.get('webhook')
        if name and discordId :
            try:
                new_user = User(name=name,discordId=discordId,webhook=webhook)
                print(new_user.name)
                db.session.add(new_user)
                db.session.commit()
            except:
                flash(message='User already is already in',category='error')
                return render_template("home.html",methods=['GET','POST'])
        else :
            flash(message='Empty user',category='error')
        return render_template("home.html",methods=['GET','POST'])
   
    return render_template("home.html",methods=['GET','POST'])

@views.route('/manga',methods=['GET','POST'])
def notifications():
    if request.method == "POST":
        users = User.query.all()
        user = request.args.get('user')
        id = User.query.filter_by(name=user).first()
        url = request.form.get('manga') 
        mangas = id.manga
        for manga in mangas:
            if url in manga.url:
                flash('Manga already in the list',category='error')
                return render_template("notifications.html",methods=['GET','POST'],users=users,user=id,manga=mangas)
        manga = scrapeManga(url=url)
        manga.userId = id.id
        db.session.add(manga)
        db.session.commit()
        print(manga.imgUrl)
        return render_template("notifications.html",methods=['GET','POST'],users=users,user=id,manga=mangas)
    elif request.method == 'GET':
        users = User.query.all()
        user = request.args.get('user')
        if user:
            id = User.query.filter_by(name=user).first()
            mangas = id.manga
            return render_template("notifications.html",methods=['GET','POST'],users=users,user=id,manga=mangas)
        return render_template("notifications.html",methods=['GET','POST'],users=users,user=user)
        
    return render_template("notifications.html",methods=['GET','POST'])

@views.route('/changeUser', methods=['POST'])
def changeUser():
    users = User.query.all()
    useR = json.loads(request.data)
    user = useR['user']
    return redirect(url_for('views.notifications',user=user,**request.args))

@views.route('/delete-manga',methods=['POST'])
def deleteManga():
    manga = json.loads(request.data)
    mangaId = manga['mangaId'] 
    url = manga['url']
    manga = Manga.query.get(mangaId)
    if manga :
        db.session.delete(manga)
        db.session.commit()
        return redirect(url)
