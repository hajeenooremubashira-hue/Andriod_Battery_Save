from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route that renders the HTML form
@app.route('/')
def home():
    return render_template('index.html')

# Route for processing battery saving options
@app.route('/optimize', methods=['POST'])
def optimize_battery():
    brightness = request.form.get('brightness')  # Get selected brightness level
    timeout = int(request.form.get('timeout'))   # Get timeout value
    apps = request.form.getlist('apps')  # Get list of apps selected for closing

    # Logic for estimating increased screen time (in hours)
    increased_time = calculate_screen_time_increase(brightness, timeout, len(apps))

    # Redirect to result page with the optimization details and increased screen time
    return redirect(url_for('show_result', brightness=brightness, timeout=timeout, apps=",".join(apps), increased_time=increased_time))

# Function to calculate the estimated screen time increase based on settings
def calculate_screen_time_increase(brightness, timeout, apps_closed):
    base_increase = 1  # Base increase in hours

    # Adjust based on brightness
    if brightness == 'low':
        base_increase += 2  # Add 2 hours for low brightness
    elif brightness == 'medium':
        base_increase += 1  # Add 1 hour for medium brightness

    # Adjust based on screen timeout (shorter timeouts save more battery)
    if timeout <= 5:
        base_increase += 1  # Shorter timeout saves battery
    elif timeout > 15:
        base_increase -= 0.5  # Longer timeouts use more battery

    # Adjust based on number of apps closed
    base_increase += apps_closed * 0.5  # Each closed app adds 0.5 hour of battery life

    return round(base_increase, 2)  # Return the estimated increase rounded to 2 decimal places

# Route for displaying the result page
@app.route('/result')
def show_result():
    brightness = request.args.get('brightness')
    timeout = request.args.get('timeout')
    apps = request.args.get('apps').split(',')
    increased_time = request.args.get('increased_time')

    return render_template('result.html', brightness=brightness, timeout=timeout, apps=apps, increased_time=increased_time)

if __name__ == '__main__':
    app.run(debug=True)
