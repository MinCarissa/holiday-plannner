from flask import Flask,request,render_template
import numpy as np
import pandas as pd


app=Flask(__name__)


## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/worker_id',methods=['post'])
def request_vac():
    employee_id = request.form.get('employee_id')
    cols = [
        'id','author','status', 'resolved_by', 
        'request_created_at', 'vacation_start_date','vacation_end_date' 
    ]
    df = pd.read_csv('Data/employees.csv', usecols = cols)
    df_worker = df[df['author']==employee_id]
    print("employee_id: ",request.form.get('employee_id'))
    print(df['author'].to_list())
    return render_template(
            'index.html',
            res_employee = "Employee ID does not exist!"
        )

@app.route('/manager/overlapping', methods=['GET'])
def get_overlapping():
    return render_template('index.html') 



@app.route('/worker/edit',methods=['post'])
def edit_employee():
    print(request.form.to_dict())
    if request.method == 'post': 
        print(">>> POST")
    employee_id = request.form.get('employee_id')
    cols = [
        'id','author','status', 'resolved_by', 
        'request_created_at', 'vacation_start_date','vacation_end_date' 
    ]
    df = pd.read_csv('Data/employees.csv', usecols = cols)
    print("employee_id: ",request.form.get('employee_id'))
    print(df['author'].to_list())
    res_employee = ""
    df_worker = df[df['author']==employee_id]
    # check if employee_id exist
    if not employee_id in df['author'].to_list():
            return render_template(
                'index.html',
                res_employee = "Employee ID does not exist!"
            )
    return render_template("employeeEdit.html", 
                               tables=[df_worker.to_html(index=False)], 
                               employee_id = employee_id, 
                               res_employee = res_employee, 
                               header="False")

@app.route('/worker/view',methods=['post'])
def view_employee():
    print(request.form.to_dict())
    if request.method == 'post': 
        print(">>> POST")
    employee_id = request.form.get('employee_id')
    cols = [
        'id','author','status', 'resolved_by', 
        'request_created_at', 'vacation_start_date','vacation_end_date' 
    ]
    df = pd.read_csv('Data/employees.csv', usecols = cols)
    print("employee_id: ",request.form.get('employee_id'))
    print(df['author'].to_list())
    res_employee = ""
    df_worker = df[df['author']==employee_id]
    # check if employee_id exist
    if not employee_id in df['author'].to_list():
            return render_template(
                'manager.html',
                res_employee = "Employee ID does not exist!"
            )
    return render_template("employee.html", 
                               tables=[df_worker.to_html(index=False)], 
                               employee_id = employee_id, 
                               res_employee = res_employee, 
                               header="False")
    
  


@app.route('/manager',methods=['POST'])
def get_summary():
    manager_id = request.form.get('manager_id')
    manager_cols = [
        'manager_id','employee_id','name' 
    ]
    df_m = pd.read_csv('Data/managers.csv', usecols = manager_cols)
    # check if manager_id exist
    if not manager_id in df_m['manager_id'].to_list():
        return render_template(
            'index.html',
            res_manager = "Manager ID does not exist!"
        )
    else:
        cols = [
            'id','author','status', 'resolved_by', 
            'request_created_at', 'vacation_start_date','vacation_end_date' 
        ]
        df_w = pd.read_csv('Data/employees.csv', usecols = cols)
        request_count = df_w.shape[0]
        pending_count = df_w[df_w['status']== 'pending'].shape[0]
        approve_count = df_w[df_w['status']== 'approved'].shape[0]
        reject_count = df_w[df_w['status']== 'rejected'].shape[0]
        return render_template(
            "manager.html", 
            manager_id = manager_id,
            request_count = request_count,
            pending_count = pending_count,
            approve_count = approve_count,
            reject_count = reject_count
        )




if __name__=="__main__":
    app.run(host="127.0.0.1", port=5003, debug=True)        