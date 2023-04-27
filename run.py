from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort, current_app as app,send_file
import pymongo
from PIL import Image
from bson import json_util
from bson.objectid import ObjectId
from fileinput import filename
import time
import json
from datetime import datetime
import io
from datetime import date, timedelta
import random
import string



myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['ADs']
all_users = mydb['all_users']
u_api = mydb['u_api']
ad_data = mydb['AD_data']
beween_dates = mydb['beween_dates']
api_data = mydb['api_keys']


app = Flask(__name__)
app.secret_key = "T\xbf\x82ZdQ\x14\xc5rUb\x14\xcf*\x91P\x83\x92\x04\x0b\x81\x01\x18\xfc"




# beween_dates.insert_one({"db":"beween","dates":[]})





def gen_key():
	key = ''.join(random.choices(string.ascii_letters+string.digits, k=50))
	return key

def get_all_dates(d11,d22):
	
	d1 = date(int(d11.split('-')[0]),int(d11.split('-')[1]),int(d11.split('-')[2]))
	d2 = date(int(d22.split('-')[0]),int(d22.split('-')[1]),int(d22.split('-')[2]))
	d = d2-d1
	lst_s = []
	for i in range(d.days + 1):
		day = d1 + timedelta(days=i)
		lst_s.append(day.strftime('%Y-%m-%d'))
	return lst_s

def get_type_pix(typ):
	if typ == 'Leaderboard':
		var1 = 740
		var2 = 120
	elif typ == 'Large-rectangle':
		var1 = 350
		var2 = 300
	elif typ == 'Medium-rectangle':
		var1 = 320
		var2 = 270
	elif typ == 'Mobile-banner':
		var1 = 310
		var2 = 60
	elif typ == 'Wide-skyscraper':
		var1 = 180
		var2 = 700

	return [var1,var2]







# --------------- MAIN --------------------

@app.route("/")
def main():
	if session.get("login_permision"):
		if session.get("id"):
			if session.get("lvl"):
				if session.get("lvl") == 'user':
					return redirect(url_for('user_main'))
				elif session.get("lvl") == 'admin':
					return redirect(url_for('admin_main'))
				elif session.get("lvl") == 'advertiser':
					return redirect(url_for('advertiser_main'))
	return render_template("landing/index.html", page_name = 'Home')


# --------------- MAIN --------------------





# --------------- Login --------------------

@app.route("/login", methods=['GET', 'POST'])
def login():
	error_msg = ''
	if session.get("login_permision"):
		if session.get("id"):
			if session.get("lvl"):
				if session.get("lvl") == 'user':
					return redirect(url_for('user_main'))
				elif session.get("lvl") == 'admin':
					return redirect(url_for('admin_main'))
				elif session.get("lvl") == 'advertiser':
					return redirect(url_for('advertiser_main'))


	if (request.method == 'POST'):
		mail = request.form.get('email')
		passs = request.form.get('pass')
		data = all_users.find_one({'mail':mail,'pass':passs})
		if data != None:
			data['_id'] = str(data['_id'])
			if data['lvl'] == 'user':
				session['login_permision'] = 1
				session['id'] = data['_id']
				session['lvl'] = 'user'
				return redirect(url_for('user_main'))

			elif data['lvl'] == 'admin':
				session['login_permision'] = 1
				session['id'] = data['_id']
				session['lvl'] = 'admin'
				return redirect(url_for('admin_main'))

			elif data['lvl'] == 'advertiser':
				session['login_permision'] = 1
				session['id'] = data['_id']
				session['lvl'] = 'advertiser'
				return redirect(url_for('advertiser_main'))

		else:
			error_msg = 'Wrong Email or Password'

	return render_template("login/login.html", page_name='login',emsg=error_msg)

# --------------- Login --------------------

# --------------- Signup --------------------

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	error_msg = ''

	if (request.method == 'POST'):
		name = request.form.get('name')
		mail = request.form.get('mail')
		passs = request.form.get('pass')
		repasss = request.form.get('repass')

		if passs == repasss:
			data = all_users.find_one({'mail':mail})
			if data == None:
				json_store = {
					"name":name,
					"mail":mail,
					"pass":passs,
					"lvl":"user"
				}
				all_users.insert_one(json_store)

				return redirect(url_for('login'))
			else:
				error_msg = 'Email is Already There'
		else:
			error_msg = 'Password and Re-Password not match'

	return render_template("login/signup.html", page_name='signup',emsg=error_msg)

# --------------- Signup --------------------

# --------------- Signup_advertiser --------------------

@app.route("/signup/advertiser", methods=['GET', 'POST'])
def signup_advertiser():
	error_msg = ''

	if (request.method == 'POST'):
		name = request.form.get('name')
		mail = request.form.get('mail')
		passs = request.form.get('pass')
		repasss = request.form.get('repass')

		if passs == repasss:
			data = all_users.find_one({'mail':mail})
			if data == None:
				json_store = {
					"name":name,
					"mail":mail,
					"pass":passs,
					"lvl":"advertiser"
				}
				all_users.insert_one(json_store)
				return redirect(url_for('login'))
			else:
				error_msg = 'Email is Already There'
		else:
			error_msg = 'Password and Re-Password not match'

	return render_template("login/signup_ad.html", page_name="Advertiser Signup",emsg=error_msg)

# --------------- Signup_advertiser --------------------

# --------------- LOGOUT --------------------

@app.route("/logout")
def logout():
	session.clear()
	return redirect('/login')

# --------------- LOGOUT --------------------

















# --------------- Advertiser --------------------

@app.route("/advertiser")
def advertiser_main():
	print(session.get("lvl"))
	if session.get("login_permision"):
		pass
	else:
		return redirect(url_for('login'))
	all_ads = ad_data.find({'uid':session.get("id")})
	if (request.method == 'POST'):
		pass

	return render_template("advertiser/index.html", page_name = 'Advertiser - Home',tot_ads=all_ads)


@app.route("/advertiser/offers")
def advertiser_offers():
	if session.get("login_permision"):
		pass
	else:
		return redirect(url_for('login'))
	return render_template("advertiser/offers.html", page_name = 'Advertiser - offers')



@app.route("/advertiser/delete", methods=['GET', 'POST'])
def advertiser_delete():
	idd = request.args.get('id')
	ad_data.delete_one({'_id':ObjectId(idd)})
	return redirect(url_for('advertiser_main'))

@app.route("/advertiser/insert", methods=['GET', 'POST'])
def advertiser_insert():
	emsg=''
	if session.get("login_permision"):
		pass
	else:
		return redirect(url_for('login'))
	if session.get("login_permision"):
		if session.get("id"):
			if session.get("lvl"):
				if session.get("lvl") == 'user':
					return redirect(url_for('user_main'))
				elif session.get("lvl") == 'admin':
					return redirect(url_for('admin_main'))
				elif session.get("lvl") == 'advertiser':
					pass

	if (request.method == 'POST'):
		ad_name = request.form.get('ad_name')
		ad_type = request.form.get('ad_type')
		link = request.form.get('link')
		sdate = request.form.get('sdate')
		edate = request.form.get('edate')
		img_data = request.files['file']
		image = Image.open(img_data)
		print(image.width,image.height)
		if ad_type == 'Leaderboard':
			if (image.width >= 700 or image.width <= 730 ) and (image.height == 90):
				pass
			else:
				emsg = 'Your Image Size is not Proper'
		elif ad_type == 'Large-rectangle':
			if (image.width >= 330 or image.width <= 340 ) and (image.height == 280):
				pass
			else:
				emsg = 'Your Image Size is not Proper'
		elif ad_type == 'Medium-rectangle':
			if (image.width == 300 ) and (image.height == 250):
				pass
			else:
				emsg = 'Your Image Size is not Proper'
		elif ad_type == 'Mobile-banner':
			if (image.width == 300 ) and (image.height == 50):
				pass
			else:
				emsg = 'Your Image Size is not Proper'
		elif ad_type == 'Wide-skyscraper':
			if (image.width == 160 ) and (image.height >= 600 or image.height >= 700 ):
				pass
			else:
				emsg = 'Your Image Size is not Proper'
		else:
			emsg = 'Select AD Type'
		new_name_img = ad_name+'_'+sdate+'_'+edate+'.'+((img_data.filename).split('.'))[-1]
		(image.convert('RGB')).save('static/ads/'+new_name_img)

		json_to_add = {
			'uid':session.get("id"),
			'ad_name':ad_name,
			'ad_type':ad_type,
			'link':link,
			'sdate':sdate,
			'edate':edate,
			'img_name':new_name_img,
			'view_cnt':0
		}
		ad_data.insert_one(json_to_add)

		return redirect(url_for('advertiser_main'))


	return render_template("advertiser/inster.html", page_name = 'Advertiser - Inster',emsg=emsg)






@app.route("/advertiser/offers/insert", methods=['GET', 'POST'])
def advertiser_offer_insert():
	emsg=''
	if session.get("login_permision"):
		pass
	else:
		return redirect(url_for('login'))
	if session.get("login_permision"):
		if session.get("id"):
			if session.get("lvl"):
				if session.get("lvl") == 'user':
					return redirect(url_for('user_main'))
				elif session.get("lvl") == 'admin':
					return redirect(url_for('admin_main'))
				elif session.get("lvl") == 'advertiser':
					pass
	id_ = 0
	if (request.method == 'GET'):
		id_ = int(request.args.get('id'))+1
	if (request.method == 'POST'):
		hid_data = int(request.form.get('hid_data'))
		for hid in range(1,hid_data+1):
			ad_name = request.form.get('ad_name'+str(hid))
			ad_type = request.form.get('ad_type'+str(hid))
			link = request.form.get('link'+str(hid))
			sdate = request.form.get('sdate')
			edate = request.form.get('edate')
			photo_file_name = 'up_photo'+str(hid)
			print(photo_file_name)
			img_data = request.files[photo_file_name]
			image = Image.open(img_data)
			print(image.width,image.height)
			if ad_type == 'Leaderboard':
				if (image.width >= 700 or image.width <= 730 ) and (image.height == 90):
					pass
				else:
					emsg = 'Your Image Size is not Proper'
			elif ad_type == 'Large-rectangle':
				if (image.width >= 330 or image.width <= 340 ) and (image.height == 280):
					pass
				else:
					emsg = 'Your Image Size is not Proper'
			elif ad_type == 'Medium-rectangle':
				if (image.width == 300 ) and (image.height == 250):
					pass
				else:
					emsg = 'Your Image Size is not Proper'
			elif ad_type == 'Mobile-banner':
				if (image.width == 300 ) and (image.height == 50):
					pass
				else:
					emsg = 'Your Image Size is not Proper'
			elif ad_type == 'Wide-skyscraper':
				if (image.width == 160 ) and (image.height >= 600 or image.height >= 700 ):
					pass
				else:
					emsg = 'Your Image Size is not Proper'
			else:
				emsg = 'Select AD Type'
			new_name_img = ad_name+'_'+sdate+'_'+edate+'.'+((img_data.filename).split('.'))[-1]
			(image.convert('RGB')).save('static/ads/'+new_name_img)
	
			json_to_add = {
				'uid':session.get("id"),
				'ad_name':ad_name,
				'ad_type':ad_type,
				'link':link,
				'sdate':sdate,
				'edate':edate,
				'img_name':new_name_img,
				'view_cnt':0
			}
			ad_data.insert_one(json_to_add)
	
		return redirect(url_for('advertiser_main'))


	return render_template("advertiser/inster_offer.html", page_name = 'Advertiser - Inster',emsg=emsg,id_=id_)

# --------------- Advertiser --------------------











# --------------- Users --------------------

@app.route("/user", methods=['GET', 'POST'])
def user_main():
	link=[]
	if session.get("login_permision"):
		pass
	else:
		return redirect(url_for('login'))
	check_api = api_data.find({"uid":session.get('id')})
	if check_api != None:
		for x in check_api:
			x['_id']=str(x['_id'])
			# print(x)
			link.append(x)
	# print(link)

	if (request.method == 'POST'):
		type_ = request.form.get('ad_type')

		var = get_type_pix(type_)
		var1 = var[0]
		var2 = var[1]
		if type_ == 'None':
			return redirect(url_for('user_main'))
		if link != None:
			flg = 0
			for x in link:
				if x['type'] == type_:
					flg = 1
			if flg == 0:
				key = gen_key()
				link = "<iframe src='http://127.0.0.1:5001/api/view/ad?key={}' height='{}' width='{}' style='border: 0px;'></iframe>".format(key,var2,var1)
				api_key_json = {
					"uid":session.get('id'),
					"type":type_,
					"key":key,
					"link":link
				}
				api_data.insert_one(api_key_json)
				return redirect(url_for('user_main'))
		else:
			key = gen_key()
			link = "<iframe src='http://127.0.0.1:5001/api/view/ad?key="+key+"' height='' width='' style='border: 0px;'></iframe>"
			api_key_json = {
				"uid":session.get('id'),
				"type":type_,
				"key":key,
				"link":link
			}
			api_data.insert_one(api_key_json)
			return redirect(url_for('user_main'))

	return render_template("user/index.html", page_name = 'User - Home',link=link)


# --------------- Users --------------------









# --------------- API --------------------

@app.route("/api/delete")
def del_api():
	id__ = request.args.get('id')
	api_data.delete_one({'_id':ObjectId(id__)})
	return redirect(url_for('user_main'))

@app.route("/api/view/ad", methods=['GET', 'POST'])
def view_ad_api():
	key = request.args.get('key')
	data = api_data.find_one({'key':key})
	if data != None:
		sdata = ''
		anc =''
		id__ = ''
		lst_tmp = []
		for x in ad_data.find({'ad_type':data['type'],'sdate':date.today().strftime("%Y-%m-%d")}):
			cnt = 1
			tmp_j = {
			"sdata" : x['img_name'],
			"anc" : x['link']
			}
			id__ = str(x['_id'])
			lst_tmp.append(tmp_j)
			cnt = cnt+x['view_cnt']
			ad_data.update_one( { "_id": ObjectId(id__) } , { "$set": { "view_cnt": cnt} } )

	return render_template("api/ad.html",page_name='ADs - API',full_img=lst_tmp)



# --------------- API --------------------















# @app.errorhandler(Exception)
# def exception_handler(error):
# 	return repr(error)









app.run(debug = True, threaded=True, host='0.0.0.0', port=5004)