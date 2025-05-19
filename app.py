from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for Flask-WTF

# Load the model and metadata
model = joblib.load('models/stress_predictor.pkl')
metadata = joblib.load('models/metadata.pkl')

# Form class for stress tracking
class StressTrackingForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=100)])
    gender = SelectField('Gender', 
                        choices=['Male', 'Female', 'Non-binary', 'Prefer not to say'],
                        validators=[DataRequired()])
    job_role = SelectField('Job Role',
                          choices=['HR', 'Data Scientist', 'Sales', 'Software Engineer', 
                                 'Designer', 'Project Manager', 'Marketing', 'Other'],
                          validators=[DataRequired()])
    industry = SelectField('Industry',
                         choices=['Healthcare', 'IT', 'Manufacturing', 'Education', 
                                'Retail', 'Finance', 'Consulting', 'Other'],
                         validators=[DataRequired()])
    years_of_experience = FloatField('Years of Experience', 
                                   validators=[DataRequired(), NumberRange(min=0, max=50)])
    work_location = SelectField('Work Location',
                              choices=['Hybrid', 'Remote', 'Onsite'],
                              validators=[DataRequired()])
    hours_worked_per_week = IntegerField('Hours Worked Per Week',
                                       validators=[DataRequired(), NumberRange(min=0, max=168)])
    virtual_meetings = IntegerField('Number of Virtual Meetings',
                                  validators=[DataRequired(), NumberRange(min=0)])
    work_life_balance = IntegerField('Work Life Balance Rating (1-10)',
                                   validators=[DataRequired(), NumberRange(min=1, max=10)])
    mental_health_resources = SelectField('Access to Mental Health Resources',
                                        choices=['Yes', 'No'],
                                        validators=[DataRequired()])
    productivity_change = SelectField('Productivity Change',
                                    choices=['Decrease', 'Increase', 'No Change'],
                                    validators=[DataRequired()])
    social_isolation = IntegerField('Social Isolation Rating (1-10)',
                                  validators=[DataRequired(), NumberRange(min=1, max=10)])
    remote_work_satisfaction = SelectField('Satisfaction with Remote Work',
                                         choices=['Unsatisfied', 'Satisfied', 'Neutral'],
                                         validators=[DataRequired()])
    company_support = IntegerField('Company Support for Remote Work (1-5)',
                                 validators=[DataRequired(), NumberRange(min=1, max=5)])
    physical_activity = SelectField('Physical Activity',
                                  choices=['Weekly', 'None', 'Daily'],
                                  validators=[DataRequired()])
    sleep_quality = SelectField('Sleep Quality',
                              choices=['Good', 'Poor', 'Average'],
                              validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    submit = SubmitField('Submit')

def get_recommendations(stress_level):
    recommendations = {
        'songs': [],
        'movies': [],
        'activities': []
    }
    
    if stress_level < 33:
        recommendations['songs'] = [
            'Happy - Pharrell Williams',
            'Here Comes the Sun - The Beatles',
            'Three Little Birds - Bob Marley'
        ]
        recommendations['movies'] = [
            'The Secret Life of Walter Mitty',
            'Soul',
            'The Intouchables'
        ]
        recommendations['activities'] = [
            'Take a short walk in nature',
            'Practice gratitude journaling',
            'Light stretching exercises'
        ]
    elif stress_level < 60:
        recommendations['songs'] = [
            'Weightless - Marconi Union',
            'River Flows in You - Yiruma',
            'Somewhere Over the Rainbow - Israel Kamakawiwoole'
        ]
        recommendations['movies'] = [
            'The Pursuit of Happyness',
            'Big Fish',
            'Little Miss Sunshine'
        ]
        recommendations['activities'] = [
            'Try a 10-minute meditation session',
            'Practice deep breathing exercises',
            'Take a relaxing bath'
        ]
    else:
        recommendations['songs'] = [
            'Clair de Lune - Debussy',
            'Gymnopédie No.1 - Erik Satie',
            'Ocean Waves White Noise'
        ]
        recommendations['movies'] = [
            'Inside Out',
            'Good Will Hunting',
            'Dead Poets Society'
        ]
        recommendations['activities'] = [
            'Schedule a therapy session',
            'Practice progressive muscle relaxation',
            'Try yoga for stress relief'
        ]
    
    return recommendations

def prepare_input_data(form_data):
    # Create a dictionary with the form data
    input_data = {
        'Age': form_data.age.data,
        'Gender': form_data.gender.data,
        'Job_Role': form_data.job_role.data,
        'Industry': form_data.industry.data,
        'Years_of_Experience': form_data.years_of_experience.data,
        'Work_Location': form_data.work_location.data,
        'Hours_Worked_Per_Week': form_data.hours_worked_per_week.data,
        'Number_of_Virtual_Meetings': form_data.virtual_meetings.data,
        'Work_Life_Balance_Rating': form_data.work_life_balance.data,
        'Access_to_Mental_Health_Resources': form_data.mental_health_resources.data,
        'Productivity_Change': form_data.productivity_change.data,
        'Social_Isolation_Rating': form_data.social_isolation.data,
        'Satisfaction_with_Remote_Work': form_data.remote_work_satisfaction.data,
        'Company_Support_for_Remote_Work': form_data.company_support.data,
        'Physical_Activity': form_data.physical_activity.data,
        'Sleep_Quality': form_data.sleep_quality.data,
        'Region': form_data.region.data
    }
    
    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Add interaction features
    input_df['Work_Pressure'] = input_df['Hours_Worked_Per_Week'] * input_df['Number_of_Virtual_Meetings'] / 100
    input_df['Support_Balance'] = input_df['Company_Support_for_Remote_Work'] * input_df['Work_Life_Balance_Rating'] / 10
    
    return input_df

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = StressTrackingForm()
    if form.validate_on_submit():
        # Prepare the input data
        input_data = prepare_input_data(form)
        
        # Make prediction using the pipeline
        stress_score = model.predict(input_data)[0]
        
        # Get recommendations based on stress score
        recommendations = get_recommendations(stress_score)
        
        return render_template('results.html',
                             stress_score=round(stress_score, 1),
                             recommendations=recommendations)
    
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True) 