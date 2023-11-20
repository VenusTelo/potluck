from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def read_from_file():
    entries = {"Main Course": [], "Side": [], "Dessert": [], "Beverage": []}
    try:
        with open('entries.txt', 'r') as file:
            for line in file:
                category, dish = line.strip().split(':')
                entries[category].append(dish.strip())
    except FileNotFoundError:
        pass
    return entries

def entry_exists(category, dish):
    return dish in dishes[category]

dishes = read_from_file()

def write_to_file():
    with open('entries.txt', 'w') as file:
        for category, dish_list in dishes.items():
            for dish in dish_list:
                file.write(f'{category}: {dish}\n')

@app.route('/')
def index():
    return render_template('index.html', dishes=dishes)

@app.route('/submit', methods=['POST'])
def submit():
    category = request.form['category']
    dish = request.form['dish']

    if entry_exists(category, dish):
        confirmation = request.form.get('confirmation', 'no')
        if confirmation == 'yes':
            dishes[category].remove(dish)
            write_to_file()
            return jsonify({'result': 'success'})
        else:
            return jsonify({'result': 'exists', 'category': category, 'dish': dish})

    dishes[category].append(dish)
    write_to_file()  # Move this line outside the if block to write changes regardless of adding or removing

    return jsonify({'result': 'success'})

@app.route('/remove', methods=['POST'])
def remove():
    category = request.form['category']
    dish = request.form['dish']

    if entry_exists(category, dish):
        dishes[category].remove(dish)
        write_to_file()
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'not_found', 'category': category, 'dish': dish})

if __name__ == '__main__':
    app.run(debug=True)

