import math
from flask import Flask, render_template, request, session
from linked_list import LinkedList
from stacks import Stack
from infixpostfix import InfixToPostfixConverter, InfixPostfixError
from queues import Queue
app = Flask(__name__)
app.secret_key = 'flask-intro-secret-key-2026'
def to_uppercase(text: str) -> str:
    if text is None or not str(text).strip():
        raise ValueError("Input string cannot be empty. Please enter text to convert.")
    clean_text = str(text).strip()
    if len(clean_text) > 1000:
        raise ValueError("Input string is too long (maximum 1,000 characters allowed).")
    if not any(c.isalpha() for c in clean_text):
        raise ValueError("Input must contain at least one alphabetic letter (a-z) to convert to uppercase.")
    return clean_text.upper()
def calculate_circle_area(radius) -> float:
    if radius is None or not str(radius).strip():
        raise ValueError("Radius input cannot be empty. Please enter a positive number.")
    clean_radius = str(radius).strip()
    try:
        r = float(clean_radius)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid radius '{clean_radius}'. Please enter a valid numeric value (e.g., 5 or 2.5).")
    if math.isnan(r) or math.isinf(r):
        raise ValueError("Radius must be a valid finite number.")
    if r <= 0:
        raise ValueError("Radius must be a positive number greater than zero.")
    if r > 10_000_000:
        raise ValueError("Radius value is too large (maximum allowed is 10,000,000).")
    return round(math.pi * (r ** 2), 2)
def calculate_triangle_area(base, height) -> float:
    if base is None or not str(base).strip():
        raise ValueError("Base input cannot be empty. Please enter a positive number.")
    if height is None or not str(height).strip():
        raise ValueError("Height input cannot be empty. Please enter a positive number.")
    clean_base = str(base).strip()
    clean_height = str(height).strip()
    try:
        b = float(clean_base)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid base '{clean_base}'. Base must be a valid numeric value.")
    try:
        h = float(clean_height)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid height '{clean_height}'. Height must be a valid numeric value.")
    if math.isnan(b) or math.isinf(b) or math.isnan(h) or math.isinf(h):
        raise ValueError("Base and height must be valid finite numbers.")
    if b <= 0:
        raise ValueError("Base must be a positive number greater than zero.")
    if h <= 0:
        raise ValueError("Height must be a positive number greater than zero.")
    if b > 10_000_000 or h > 10_000_000:
        raise ValueError("Dimensions are too large (maximum allowed is 10,000,000).")
    return round(0.5 * b * h, 2)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/works', methods=['GET', 'POST'])
def works():
    result = None
    error = None
    input_string = ''
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        try:
            result = to_uppercase(input_string)
        except ValueError as e:
            error = str(e)
    return render_template('touppercase.html', result=result, error=error, input_string=input_string)
@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    error = None
    radius = ''
    if request.method == 'POST':
        radius = request.form.get('radius', '')
        try:
            result = calculate_circle_area(radius)
        except ValueError as e:
            error = str(e)
    return render_template('circle.html', result=result, error=error, radius=radius)
@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None
    error = None
    base = ''
    height = ''
    if request.method == 'POST':
        base = request.form.get('base', '')
        height = request.form.get('height', '')
        try:
            result = calculate_triangle_area(base, height)
        except ValueError as e:
            error = str(e)
    return render_template('triangle.html', result=result, error=error, base=base, height=height)
@app.route('/works/linkedlist', methods=['GET', 'POST'])
@app.route('/works/linked-list', methods=['GET', 'POST'])
def linked_list_demo():
    if 'linked_list' not in session or not isinstance(session['linked_list'], list):
        session['linked_list'] = ["Apple", "Banana", "Cherry"]
    ll = LinkedList.from_list(session['linked_list'])
    message = None
    error = None
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        data = request.form.get('data', '')
        target = request.form.get('target', '')
        try:
            if action == 'insertatbeginning':
                ll.insertatbeginning(data)
                message = f"Successfully inserted '{data.strip()}' at beginning."
            elif action == 'insertatend':
                ll.insertatend(data)
                message = f"Successfully inserted '{data.strip()}' at end."
            elif action == 'insertafter':
                ll.insertafter(target, data)
                message = f"Successfully inserted '{data.strip()}' after '{target.strip()}'."
            elif action == 'removeatbeginning':
                removed = ll.removeatbeginning()
                message = f"Successfully removed '{removed}' from beginning."
            elif action == 'removeatend':
                removed = ll.removeatend()
                message = f"Successfully removed '{removed}' from end."
            elif action == 'removetarget':
                removed = ll.removetarget(target)
                message = f"Successfully removed '{removed}' from list."
            elif action == 'reset':
                ll = LinkedList.from_list(["Apple", "Banana", "Cherry"])
                message = "Linked list reset to default sample."
            else:
                raise ValueError(f"Unknown action '{action}'.")
            session['linked_list'] = ll.to_list()
        except (ValueError, IndexError, OverflowError) as err:
            error = str(err)
    return render_template('linked_list.html', nodes=ll.to_list(), message=message, error=error)
@app.route('/works/stack', methods=['GET', 'POST'])
@app.route('/works/stacks', methods=['GET', 'POST'])
def stack_demo():
    if 'stack' not in session or not isinstance(session['stack'], list):
        session['stack'] = ["Plate 1", "Plate 2", "Plate 3"]
    stack = Stack.from_list(session['stack'])
    message = None
    error = None
    peek_item = None
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        data = request.form.get('data', '')
        try:
            if action == 'push':
                stack.push(data)
                message = f"Successfully pushed '{data.strip()}' onto the top of the stack."
            elif action == 'pop':
                popped = stack.pop()
                message = f"Successfully popped '{popped}' from the top of the stack."
            elif action == 'peek':
                peek_item = stack.peek()
                message = f"Top element is '{peek_item}'."
            elif action == 'clear':
                stack.clear()
                message = "Stack has been cleared."
            elif action == 'reset':
                stack = Stack.from_list(["Plate 1", "Plate 2", "Plate 3"])
                message = "Stack reset to default sample."
            else:
                raise ValueError(f"Unknown action '{action}'.")
            session['stack'] = stack.to_list()
        except (ValueError, IndexError, OverflowError) as err:
            error = str(err)
    return render_template('stack.html', items=stack.to_list(), message=message, error=error, peek_item=peek_item)
@app.route('/works/infixpostfix', methods=['GET', 'POST'])
@app.route('/works/infix-postfix', methods=['GET', 'POST'])
def infix_postfix_demo():
    expression = ''
    postfix_result = None
    steps = []
    error = None
    if request.method == 'POST':
        expression = request.form.get('expression', '')
        try:
            postfix_result, steps = InfixToPostfixConverter.convert_with_steps(expression)
        except InfixPostfixError as err:
            error = str(err)
        except Exception as err:
            error = f"Unexpected error: {err}"
    return render_template('infix_postfix.html', expression=expression, postfix_result=postfix_result, steps=steps, error=error)
@app.route('/works/queue', methods=['GET', 'POST'])
@app.route('/works/queues', methods=['GET', 'POST'])
def queue_demo():
    if 'queue' not in session or not isinstance(session['queue'], list):
        session['queue'] = ["Customer A", "Customer B", "Customer C"]
    q = Queue.from_list(session['queue'])
    message = None
    error = None
    peek_item = None
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        data = request.form.get('data', '')
        try:
            if action in ('enqueue', 'queue'):
                q.enqueue(data)
                message = f"Successfully enqueued '{data.strip()}' at the rear (tail)."
            elif action == 'dequeue':
                dequeued = q.dequeue()
                message = f"Successfully dequeued '{dequeued}' from the front (head)."
            elif action in ('peek', 'front'):
                peek_item = q.peek()
                message = f"Front element is '{peek_item}'."
            elif action == 'clear':
                q.clear()
                message = "Queue has been cleared."
            elif action == 'reset':
                q = Queue.from_list(["Customer A", "Customer B", "Customer C"])
                message = "Queue reset to default sample."
            else:
                raise ValueError(f"Unknown action '{action}'.")
            session['queue'] = q.to_list()
        except (ValueError, IndexError, OverflowError) as err:
            error = str(err)
    return render_template('queue.html', items=q.to_list(), message=message, error=error, peek_item=peek_item)
@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contacts', methods=['GET', 'POST'])
def contact():
    message_sent = False
    if request.method == 'POST':
        message_sent = True
    return render_template('contact.html', message_sent=message_sent)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
