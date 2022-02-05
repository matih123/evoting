from evoting import app, my_voting, voters
from flask import render_template, redirect, url_for, flash, make_response, request
from evoting.forms import LoginForm
from evoting.bcrypt import *
from evoting.models import User
from flask_login import login_user, current_user, logout_user, login_required
from evoting.voting import *

@app.route('/', methods=['GET', 'POST'])
def home():
    if hasattr(current_user, 'id') and isinstance(current_user.id, str):
        return render_template('vote.html', candidates=my_voting.list_of_candidates, len_candidates=my_voting.number_of_candidates)

    form = LoginForm()
    if form.validate_on_submit():
        pesel = form.pesel.data
        if verify_user(pesel, form.password.data):
            user = User(pesel)
            login_user(user)
            return render_template('vote.html', candidates=my_voting.list_of_candidates, len_candidates=my_voting.number_of_candidates)
        
    return render_template('home.html', form=form)

@app.route("/logout", methods=['GET'])
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/vote", methods=['POST'])
def vote():
    v = request.form.get('vote')
    if hasattr(current_user, 'id') and isinstance(current_user.id, str) and v is not None:
        if current_user.id not in voters:
            voters.append(current_user.id)
            user_vote = [0 for _ in range(my_voting.number_of_candidates)]
            user_vote[int(v)] = 1
            encrypted_vote = my_voting.vote(user_vote)
            hashed = my_voting.hash_vote(encrypted_vote)

            return render_template('confirm_vote.html', hashed=hashed)
        else:
            r = make_response('User voted already.', 400)
            r.mimetype = 'text/plain'
            return r
    else:
        r = make_response('User is not authenticated.', 400)
        r.mimetype = 'text/plain'
        return r

@app.route("/votes_list", methods=['GET'])
def votes_list():
    hashes = [my_voting.hash_vote(v) for v in my_voting.encrypted_votes]
    return render_template('votes_list.html', hashes=hashes)

@app.route("/results", methods=['GET'])
def results():
    my_voting.export_public_info('evoting/static/results.py')
    return render_template('results.html', results=my_voting.get_results(), candidates=my_voting.list_of_candidates, len_candidates=my_voting.number_of_candidates)
