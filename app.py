from typing import Optional
from flask import Flask, render_template, request, redirect, url_for
from data.zodiac_data import zodiac_info
from data.db import save_feedback_to_database, get_feedback_from_database
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/date')
def date():
    return render_template('date.html')


@app.route('/process_date', methods=['POST'])
def process_date():
    day = int(request.form['day'])
    month = int(request.form['month'])
    zodiac_sign = get_zodiac_sign(day, month)
    # Redirect the user to the result page with the zodiac sign as a query parameter
    return redirect(url_for('result', zodiac_sign=zodiac_sign))


def get_zodiac_sign(day: int, month: int) -> Optional[str]:
    # Define the zodiac signs and their corresponding date ranges
    zodiac_data = {
        "Aries": {"start_date": (3, 21), "end_date": (4, 20)},
        "Taurus": {"start_date": (4, 21), "end_date": (5, 20)},
        "Gemini": {"start_date": (5, 21), "end_date": (6, 20)},
        "Cancer": {"start_date": (6, 21), "end_date": (7, 21)},
        "Leo": {"start_date": (7, 22), "end_date": (8, 22)},
        "Virgo": {"start_date": (8, 23), "end_date": (9, 22)},
        "Libra": {"start_date": (9, 23), "end_date": (10, 22)},
        "Scorpio": {"start_date": (10, 23), "end_date": (11, 21)},
        "Ophiuchus": {"start_date": (11, 27), "end_date": (12, 17)},  # Including Ophiuchus
        "Sagittarius": {"start_date": (11, 22), "end_date": (12, 21)},
        "Capricorn": {"start_date": (12, 22), "end_date": (1, 19)},
        "Aquarius": {"start_date": (1, 20), "end_date": (2, 19)},
        "Pisces": {"start_date": (2, 20), "end_date": (3, 20)},
    }

    # Check for the zodiac sign based on the date provided
    for sign, dates in zodiac_data.items():
        start_month, start_day = dates["start_date"]
        end_month, end_day = dates["end_date"]
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return sign


@app.route('/result/<zodiac_sign>') # type: ignore
def result(zodiac_sign):
    # Ensure zodiac_sign exists in zodiac_info to prevent KeyError
    zodiac_info_entry = zodiac_info.get(zodiac_sign)
    if zodiac_info_entry:
        return render_template('result.html', zodiac_sign=zodiac_sign, zodiac_info=zodiac_info_entry)



@app.route('/save_feedback/<zodiac_sign>', methods=['POST'])
def save_feedback(zodiac_sign):
    name = request.form['name']
    comment = request.form['comment']
    rating = int(request.form['rating'])

    # Save the feedback to the database
    save_feedback_to_database(name, comment, rating, zodiac_sign)

    return redirect(url_for('feedback'))  # Redirect to the feedback page



@app.route('/feedback')
def feedback():
    feedback_data = get_feedback_from_database()
    print("Feedback data from database:", feedback_data)  # Add this line for debugging
    return render_template('feedback.html', feedback_data=feedback_data)

if __name__ == '__main__':
    app.run(debug=True)
