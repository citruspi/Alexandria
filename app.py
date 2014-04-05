from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config.Debug')

if __name__ == "__main__":

	  app.run()
