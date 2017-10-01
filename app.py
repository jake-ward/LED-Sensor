import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create dictionary called pins; store pin no., name and pin state:
pins = {
	23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW},
	24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}
}

# Set ech pin as output and make it low:
for pin in pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
	# For each pin, read state, store it in pins dictionary:
	for pin in pins:
		pins[pin]['state'] = GPIO.input(pin)
	# Put the pin dictionary into the template data dictionary:
	templateData = {
		'pins' : pins
		}
	# Pass template data into template main.html, return it to user
	return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with pin no. and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
	# Convert pin from URL into integer:
	changePin = int(changePin)
	# Get device name for pin being changed:
	deviceName = pins[changePin]['name']
	# If action part of URL is "on", execute code:
	if action == "on":
		# Set pin high:
		GPIO.output(changePin, GPIO.HIGH)
		# Save status message to be passed into template:
		message = "Turned " + deviceName + " on."
	if action == "off":
		GPIO.output(changePin,GPIO.LOW)
		message = "Turned " + deviceName + " off."

	# For each pin, read state, store in pins dictionary:
	for pin in pins:
		pins[pin]['state'] = GPIO.input(pin)

	# Put message into templateData dictionary:
	templateData = {
		'pins' : pins
	}

	return render_template('main.html', **templateData)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
