from datetime import datetime
from multiprocessing.connection import wait
import requests
from website import creat_app
from flask_apscheduler  import APScheduler
from website.models import User,Manga
from website.scrape import scrapeForChapters, scrapeName,scrapeForChapter
from website import db
import json,time

def schedule():
    with app.app_context():
        users = User.query.all()
        for user in users:
            mangas = user.manga
            for manga in mangas:
                time.sleep(2)
                scrap = scrapeForChapter(manga.url)
                date = scrap[0]
                nr = int(scrap[1])
                nrChapters = nr - int(manga.nrOfChapters)
                if date == manga.lastChapterDate:
                    print(f"Up to date {manga.name}")

                if date > manga.lastChapterDate:
                    manga.lastChapterDate = date
                    manga.nrOfChapetrs = nr
                    db.session.commit()
                    data = {"content":"New manga BITCH <@"+str(user.discordId)+"> "+manga.name,"embeds":[{"title":manga.name,"url":scrap[2],"fields":[{"name":"Nr of chapters realeased","value":nrChapters}],"image":{"url":manga.imgUrl}}]}
                    x = requests.post(url='https://discord.com/api/webhooks/971088379783557181/JOyYTFkJHCYf-xwUxWOga_xzvaGgSeQ4ADNxsybUkO08rkU719Do0k_7a_Cy37U-8Q6q',json=data)
                    print(x.reason)
            print(f"Done with {user.name}'s manga")
        print("~~~~~~~")
        

app = creat_app()
scheduler = APScheduler()
scheduler.add_job(id = 'Test', func=schedule, trigger='interval', minutes = 5)   
scheduler.start()

if __name__ == '__main__':
    app.run()
    

