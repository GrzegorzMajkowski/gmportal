from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import  current_user,  login_required
from gmportal import db
from gmportal._losowa.forms import LosowaForm
from gmportal._losowa.models import LosowaTab
import random
#from gmportal import db
#from gmportal.models import User  #, BlogPost
#from gmportal._users.forms import RegistrationForm, LoginForm, UpdateUserForm
#from puppycompanyblog.users.picture_handler import add_profile_pic

losowaBP = Blueprint('losowaBP',__name__,template_folder='templates')
# ra=random.randint(1,100)
# i=0

class Losowanie():
    rnd_num=0
    wynik=''
    proba=''
    i=0
    koniec=False
    result_pile=[]
    def __init__(self):
        self.rnd_num=random.randint(1,100)
        self.result_pile=[]

    def wynik_proby(self,liczba):
        if int (liczba)==4021:
            self.wynik='Błędny wpis!'
            self.i+=1
            self.proba=f'Próba nr {self.i}'
            self.result_pile.insert(0,'error_')
        elif int(liczba)<self.rnd_num:
            self.wynik='To jest za mało1...Próbuj dalej!'
            self.i+=1
            self.proba=f'Próba nr {self.i}'
            self.result_pile.insert(0,'to_little')
        elif int(liczba)>self.rnd_num:
            self.wynik='To jest za duzo... Próbuj dalej'
            self.i+=1
            self.proba=f'Próba nr {self.i}'
            self.result_pile.insert(0,'to_much')
        elif int(liczba)==self.rnd_num:
            self.wynik='BRAWO!!! To jest właśnie ta liczba!'
            self.i+=1
            self.proba=f'Za {self.i} razem'
            self.result_pile.insert(0,'win')
            self.koniec=True




los=None


@losowaBP.route('/prelosowa',  methods=['GET', 'POST'])
@login_required
def prelosowa():
    lososowatablica = db.session.query(LosowaTab).delete()
    #db.session.delete(lososowatablica)
    db.session.commit()
    rnd_num=random.randint(1,100)
    lososowatablica = LosowaTab(rnd_num,0,0,'',current_user.username)
    db.session.add(lososowatablica)
    db.session.commit()

    return redirect(url_for('losowaBP.losowa'))


@losowaBP.route('/losowa',  methods=['GET', 'POST'])
@login_required
def losowa():
    form = LosowaForm()
    
    
    w2="To jest w2 super"

    def check_input (i):
        losowatablica = LosowaTab.query.order_by(LosowaTab.id).all()
        tablicawynikow=[]
        koniec=False
        

        for row in losowatablica:
            wynik = row.wynik
            nr_proby = row.nr_proby
            rnd_num = row.rnd_num
            wynik_msg= row.wynik_msg
            _id= row.id
            tablicawynikow.append((_id,nr_proby,wynik,wynik_msg))

        if int (i)==4021:
            komentarz_wynik='Błędny wpis!'
            wynik_msg='error_'
        elif int(i)<rnd_num:
            komentarz_wynik='To jest za mało...Próbuj dalej! db'
            wynik_msg='to_little'
        elif int(i)>rnd_num:
            komentarz_wynik='To jest za duzo... Próbuj dalej db'
            wynik_msg='to_much'
        elif int(i)==rnd_num:
            komentarz_wynik='BRAWO!!! To jest właśnie ta liczba! db'
            wynik_msg='win'
            koniec=True

        nr_proby+=1
        komentarz_proba = f'Próba nr {nr_proby}'
        wynik=i
        
        
        tablicawynikow.insert(0,(1000,nr_proby,wynik,wynik_msg))
        tablicawynikow.sort(reverse=True)
        losowatablica=LosowaTab(rnd_num,wynik,nr_proby,wynik_msg,current_user.username)
        db.session.add(losowatablica)
        db.session.commit()


        return (komentarz_wynik, komentarz_proba, wynik_msg, tablicawynikow,koniec)

    

    if form.validate_on_submit():
        n=form.input_value.data
        try:
            i=int(n)
            #losowatablica = LosowaTab.query.order_by(LosowaTab.id.desc()).first()
            #los.wynik_proby(n)
            #wynik = losowatablica.rnd_num
            #proba = losowatablica.proba+1
            #warn_msg=''
            los_tab = check_input(i)
            komentarz_wynik = los_tab[0]
            komentarz_proba = los_tab[1]
            wynik_msg = los_tab[2]
            tablicawynikow=los_tab[3]
            koniec=los_tab[4]
            warn_msg=''

        except ValueError:
            form.input_value.data='0'
            los_tab = check_input(4021)
            komentarz_wynik = los_tab[0]
            komentarz_proba = los_tab[1]
            wynik_msg = los_tab[2]
            tablicawynikow=los_tab[3]
            koniec=los_tab[4]
            warn_msg='NIWŁAŚCIWA WARTOŚĆ - MUSI BYĆ LICZBA POMIEDZY 1 a 100'
            

        form.input_value.data=''
        #return render_template('losowa.html', form=form, wynik=los.wynik, w2=los.rnd_num, proba=los.proba,koniec=los.koniec,historia=los.result_pile, warn_msg=warn_msg)
        return render_template('losowa.html', form=form, komentarz_wynik=komentarz_wynik, warn_msg=warn_msg, komentarz_proba=komentarz_proba,koniec=koniec,tablicawynikow=tablicawynikow)

    return render_template('losowa.html', form=form)


