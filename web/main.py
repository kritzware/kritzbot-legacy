from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index_page():
	return render_template('index.html')

@app.route('/commands')
def commands_page():
	return render_template('commands.html')

@app.route('/stats')
def stats_page():
	return render_template('stats.html')

@app.route('/admin')
def admin_page():
	return render_template('admin.html')

@app.route('/control-panel', methods=['GET', 'POST'])
def control_panel_page():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('admin_page'))
	return render_template('control-panel.html', error=error)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)