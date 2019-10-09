from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class ExperimenterForm(FlaskForm):
    parameter = RadioField('type', choices=[("none", "none"),
                                            ("question","question"), 
                                            ("yes/no","yes/no"), 
                                            ("statement", "statement")], validators=[DataRequired()])

    arguement_type = RadioField('arguement_type', choices=[("none" , "none"),
                                                           ("parallel", "parallel"),
                                                           ("feeling","feeling"),
                                                           ("fact","fact"),
                                                           ("socratic", "socratic")], validators=[DataRequired()])
    
    strategy = RadioField('strategy', choices=[("random", "random"),
                                                     ("retrieval", "retrieval")], validators=[DataRequired()])
    assessment = RadioField('assessment', choices=[("before", "before"),
                                                   ("both", "both"),
                                                   ("after", "after")], validators=[DataRequired()])
    submit = SubmitField('Submit')

class AssessmentForm(FlaskForm):
    agree = [("strongly disagree", "strongly disagree"),
               ("disagree", "disagree"), 
               ("neutral", "neutral"),
               ("agree", "agree"),
               ("strongly agree", "strongly agree")]
    yes = [("yes", "yes"),
           ("no", "no")]
    apathy = RadioField('you feel strongly towards this topic', choices=agree, validators=[DataRequired()])
    research = RadioField('you have done a lot of research regarding this topic', choices=agree, validators=[DataRequired()])
    openness = RadioField('you are likely to change your mind regarding this topic', choices=agree, validators=[DataRequired()])
    disscussion = RadioField('you have discussed this topic with others in the past', choices=agree, validators=[DataRequired()])
    heard = RadioField('you have previously heard of this topic', choices=yes, validators=[DataRequired()])
    submit = SubmitField('Submit')

class TopicForm(FlaskForm):
    climate_for_opinion = ("Climy: I think that the world needs to act on climate change now. The urgency is paramount. <br>"
                         "I think the climate change might be the most critical issue to face humanity")
    
    australiaDay_for_opinion = ("Aussie: I think Australia Day is celeberation that is ejoyed by vast majority of Australians.<br>"
                                "We should not change autralia day")
    
    australiaDay_not_opinion = ("Nolly: I think Australia day signifies the arival of the british and colonisation of the indegenious population. <br>"
                                "We should change the day of Australia day")
    topic = RadioField("Who would you like to debate against", choices = [("1,climate change", climate_for_opinion),
                                                                          ("-1,australia day", australiaDay_for_opinion),
                                                                          ("1,australia day", australiaDay_not_opinion)])
    submit = SubmitField('Submit')
