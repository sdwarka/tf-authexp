from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required
from datetime import datetime
from .models import Expense
from app import db
from . import exp

# helper function to extract request data into
# another dict. TODO: is this really required?
def get_expense_data(req: dict) -> dict:
    
    retval = {}
    
    #TODO: validation code
    retval['exp_date'] = req['v_exp_date']
    retval['exp_head'] = req['v_exp_head']
    retval['exp_desc'] = req['v_desc']
    retval['exp_amt' ] = req['v_amt']
    retval['exp_type'] = req['v_exp_type']
    retval['exp_mode'] = req['v_pay_mode']
    retval['exp_rem' ] = req['v_remarks']
    
    return retval

# helper function to create a URL string from
# exp_data dict. TODO: is this really required?
def get_exp_data_urlstr(exp_data: dict) -> str:
    
    retval = '?'
    retval += f'v_exp_date={exp_data["exp_date"]}&'
    retval += f'v_exp_head={exp_data["exp_head"]}&'
    retval += f'v_desc={exp_data["exp_desc"]}&'
    retval += f'v_amt={exp_data["exp_amt"]}&'
    retval += f'v_exp_type={exp_data["exp_type"]}&'
    retval += f'v_pay_mode={exp_data["exp_mode"]}&'
    retval += f'v_remarks={exp_data["exp_rem"]}&'
    
    return retval

# displays the add_expense.html input page
@exp.route('/exp', methods=['GET'])
@login_required
def add_expense_input():
    return render_template('add_exp.html')

# processes the expense data submitted from the add_expense.html input page
@exp.route('/exp', methods=['POST'])
@login_required
def add_expense_process():
    
    # extract the expense data
    exp_data = get_expense_data(request.form)
    
    # TODO: validate the expense data
    # TODO: save validated data in db
    dtformat = '%Y-%M-%d'
    dt = datetime.strptime(exp_data['exp_date'], dtformat) #db.Column(db.Date())
    cat = exp_data['exp_head'] #db.Column(db.String(100))
    desc = exp_data['exp_desc'] #
    amt  = exp_data['exp_amt'] #db.Column(db.Float())
    typ = exp_data['exp_type'] #db.Column(db.String(100))
    mode = exp_data['exp_mode'] #db.Column(db.String(100))
    rem  = exp_data['exp_rem'] #db.Column(db.String(512))

    exp_record = Expense(exp_date=dt, exp_catg=cat, exp_desc=desc,
        exp_amt=amt, exp_type=typ, exp_mode=mode, exp_rem=rem)

    print(f'storing expense {exp_data}')
    db.session.add(exp_record)
    db.session.commit()

    # TODO: remove this after fixing exp.view
    # redirect to view_expense.html page
    exp_data_urlstr = get_exp_data_urlstr(exp_data)

    return redirect(url_for('exp.view')+exp_data_urlstr)


# view list of expenses
@exp.route('/view', methods=['GET'])
@login_required
def view():
    
    ############################################################
    # 1st version; forward request params
    #exp_data = get_expense_data(request.args)
    #return render_template('view_exp.html', exp_data=exp_data)
    ############################################################

    # Fetch data from database and display
    exps = Expense.query.all()
    return render_template('view_exp.html', exp_data=exps)

