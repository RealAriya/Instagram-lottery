Instagram Lottery Project

An online Instagram lottery system built with Flask. Users can participate in lotteries based on comments, likes, or followers on Instagram posts.

Features
User authentication (register/login).
Payment
Excel generation

Lottery types: comments, likes, or followers.

Random winner selection.

Excel export for participant lists.

Payment integration for large lotteries.

Technologies
Flask, SQLAlchemy, Selenium, Bootstrap, Pandas, dotenv.

Getting Started
Prerequisites
Python 3.8+

Chrome browser

ChromeDriver (matching Chrome version)

MySQL or any SQL database

Installation
Clone the repo
git clone https://github.com/your-username/instagram-lottery.git
cd instagram-lottery
Set up a virtual environment:

python -m venv .env
source .env/bin/activate  # On Windows: .env\Scripts\activate
Install dependencies:


pip install -r requirements.txt
Set up the database:

Create a MySQL database.

Update DATABASE_URI in .envv with your credentials.

Create a .envv file:

plaintext
SECRET_KEY=your_secret_key
DATABASE_URI=mysql+pymysql://username:password@localhost/dbname
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
CHROMEDRIVER_PATH=/path/to/chromedriver
Initialize the database:


flask shell
>>> db.create_all()
>>> exit()

Run the app:
flask run
Visit http://127.0.0.1:5000.
