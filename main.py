from flask import Flask, render_template, request

app = Flask(__name__)

def file_to_dict(filename='to_do_list_file.txt'):
    file = open(filename, 'r', encoding='utf8')
    data = file.readlines()
    result = dict()
    for item in data:
        key, values = item.strip().split(':')
        values = values.split(';')
        result[key] = values
    return result

TO_DO_LIST = file_to_dict()

def write_to_file(x):
    with open('to_do_list_file.txt', 'w', encoding='utf8') as f:
        for item in x:
            f.write(item + ':' + ';'.join(x[item]) + '\n')

@app.route('/')
def engine():
    return render_template(
        'index.html',
        to_do_list_items=TO_DO_LIST
    )

@app.route('/to_do_list_form/', methods=['POST'])
def add_new_list():
    if request.form['action'] == 'add_list':
        list_name = request.form['list_name']
        TO_DO_LIST[list_name] = []
    elif request.form['action'] == 'add_act':
        act = request.form['act_name']
        list_name = request.form['lists']
        TO_DO_LIST[list_name].append(act)
    elif request.form['action'] == 'refresh':
        p = request.form['point']
        act, list_name = p.split(' - ')
        TO_DO_LIST[list_name].remove(act)
    write_to_file(TO_DO_LIST)
    return render_template(
        'index.html',
        to_do_list_items=TO_DO_LIST)

app.run('127.0.0.1', 8080)
