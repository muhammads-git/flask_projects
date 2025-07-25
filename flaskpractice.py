# @app.route('/', methods=['GET', 'POST'])
# def home():
#     name = ''
#     if request.method == 'POST':
#         name = request.form.get('username')
#     return render_template('index.html', name=name)

# @app.route('/<myname>/<int:post_id>')
# def aboutme(myname=None, post_id=None):
#     return render_template('about.html', name=myname, post_id=post_id)
