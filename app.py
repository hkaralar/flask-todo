from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "Çok gizli bir key"

# veri tabanı bağlantısı
client = MongoClient("mongodb+srv://egitim:egitim48@cluster0-wj5ww.mongodb.net/test?retryWrites=true&w=majority")
# tododb: veri tabanı adı, todos: collection ismi
db = client.tododb.todos
# artık db. ile veri tabanında her şeyi yapabilirim

@app.route('/')
def index():
    # veri tabanından kayıtları çek, bir listeye al
    yapilacaklar = []
    for yap in db.find():
        yapilacaklar.append({
            "_id":str(yap.get("_id")),
            "isim": yap.get("isim"), 
            "durum": yap.get("durum") 
        })
    # index.html'e bu listeyi gönder
    return render_template('index.html', yapilacaklar = yapilacaklar)

@app.route('/guncelle/<id>')
def guncelle(id):
    # Gelen id değeri ile kaydı bulalım
    yap = db.find({'_id':ObjectId(id)})
    # Durum değeri True ise False, False ise True yapalım
    durum = not yap.get('durum')
    # kaydı güncelle
    db.find_one_and_update(
        {'_id':ObjectId(id)},
        {'$set':{'durum':durum}})
    
    # ana sayfaya yönlendir
    return redirect('/')

@app.route('/sil/<id>')
def sil(id):
    # id'si gelen kaydı sil
    db.find_one_and_delete({'_id':ObjectId(id)})
    # ana sayfaya gönder
    return redirect('/')

@app.route('/ekle', methods = ['POST'])
def ekle():
    # Kullanıcıdan sadece isim aldık
    # durumu default olarak False kabul ediyoruz
    isim = request.form.get('isim')
    db.insert_one({'isim':isim, 'durum':'False'})
    # ana sayfaya yönlendir
    return redirect('/')

# hatalı ya da olmayan bir url isteği gelirse
# hata vermesin, ana sayfaya yönlendirelim
@app.errorhandler(404)
def hatali_url():
   return redirect('/')

@app.route('/kimiz')
def kimiz():
   return render_template('kimiz.html')

@app.route('/user/<isim>')
def user(isim):
    # ismi sayfaya gönder
    return render_template('user.html', isim = isim)   

if __name__ == '__main__':
  app.run(debug=True)
