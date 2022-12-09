
# @app.route('/form', methods=['GET', 'POST'])
# def contactform():
#     logging.debug("/form endpoint: pid: " + str(os.getpid()))
#     print("[DEBUG]/form endpoint: pid: ", str(os.getpid()))
# 	form = ContactForm()
# 	if request.method == 'GET':
# 		return render_template('contact.html', form=form)
# 	elif request.method == 'POST':
# 		if form.validate() == False:
# 			flash('All fields are required !')
# 			return render_template('contact.html', form=form)
# 		else:
# 			msg = Message(form.subject.data, sender='[SENDER EMAIL]', recipients=['your reciepients gmail id'])
# 			msg.body = """
# 			from: %s &lt;%s&gt
# 			%s
# 			"""% (form.name.data, form.email.data, form.message.data)
# 			mail.send(msg)
# 			return redirect(url_for('index'))
# 		return '<h1>Form submitted!</h1>'  


#TODO at start (or using a deamon thread) clean all images before curernt timestamp 

    # with open( pathImage, mode="rb" ) as f:
    #     imageContent = f.read().decode("iso-8859-1")
    #     #(open(input_filename, "rb").read()).decode("iso-8859-1")
    #     dict_out = {
    #         "information": "OK",
    #         "filenameWithStamp": filenameWithStamp,
    #         "stream": imageContent,
    #         "details": "none"
    #     }
    #     return dict_out


# @app.route("/getimage", methods=['GET'])
# def getImage():
#     filename = os.path.join(bufferImages.directory, bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp)
#     with open( filename, mode="rb" ) as f:
#        imageContent = f.read().decode("iso-8859-1")
#        #(open(input_filename, "rb").read()).decode("iso-8859-1")
#        dict_out = {
#            "filename": filename,
#            "stream": imageContent
#        }
#        return dict_out



# @app.route('/contact', methods=['POST', 'GET'])
# def contact():
#     form = ContactForm()
#     if form.validate_on_submit():        
#         print('-------------------------')
#         print(request.form['name'])
#         print(request.form['email'])
#         print(request.form['subject'])
#         print(request.form['message'])       
#         print('-------------------------')
#         send_message(request.form)
#         return redirect('/success')      
#     return render_template('views/contacts/contact.html', form=form)

# @app.route('/success')
# def success():
#     return redirect('/camera') # return render_template('views/home/index.html')

# def send_message(message):
#     print(message.get('name'))
#     #msg = Message(message.get('subject'), sender = message.get('email'),
#     #        recipients = ['id1@gmail.com'],
#     #        body= message.get('message')
#     #)  
#     #mail.send(msg)
