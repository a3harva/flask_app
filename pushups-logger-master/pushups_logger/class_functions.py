from email.policy import default
import re
from . import db
from .models import User
from .models import Workout
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort,jsonify

from flask_login import current_user, login_required
from flask.views import MethodView

class_functions= Blueprint('class_functions', __name__)





class Class_functions(MethodView):

    # decorators =[login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self,workout_id):
        if request.method == 'GET':
            if workout_id:
                user = User.query.filter_by(email=current_user.email).first_or_404()
                workouts = user.workouts  # Workout.query.filter_by(author=user).order_by(Workout.date_posted.desc())
        # return render_template('all_workouts.html', workouts=workouts, user=user)
                return render_template('class_functions.html',workouts=workouts,user=current_user,passed_id=workout_id)
            else:
                user = User.query.filter_by(email=current_user.email).first_or_404()
                workouts = user.workouts  
                return render_template('class_functions_all.html',workouts=workouts,user=current_user)
                

        if request.method=='POST':
            pushups = request.form.get('pushups')
            comment = request.form.get('comment')
            print(pushups, comment)
            workout = Workout(pushups=pushups, comment=comment, author=current_user)
            db.session.add(workout)
            db.session.commit()
            flash('Your workout has been added!')
            return redirect(url_for('class_functions.html'))


        if request.method =='UPDATE':
            workout = Workout.query.get_or_404(workout_id)
            workout.update_from_json(request)
            db.session.commit()
            return redirect(url_for('class_functions.html'))
        
        if request.method =='DELETE':
            workout = Workout.query.get_or_404(workout_id)
            db.session.delete(workout)
            db.session.commit()
            flash('Your post has been deleted!')    
            return redirect(url_for('class_functions.html'))
        
      

class_function_view = Class_functions.as_view('class_function')

class_functions.add_url_rule('/class_functions',defaults={'workout_id':None},view_func=class_function_view,methods=['GET',])
class_functions.add_url_rule('/class_functions/<int:workout_id>', view_func=class_function_view,methods=['GET','POST,' 'PUT', 'DELETE'])