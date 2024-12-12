from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:ConVox%404@172.16.13.92:3306/new_user"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    # Table name set to 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
   return render_template("index.html")

# Route to add a new user
@app.route('/user', methods=['POST'])
def add_user():
   
    name = request.form.get("name") 
    phone_no =request.form.get("phone_no") 
    email = request.form.get("email") 
    
    # Create a new user
    new_user = User(name=name, phone_no=phone_no, email=email)
    db.session.add(new_user)
    db.session.commit()
    return render_template("index.html")

#route to delete a user
@app.route('/delete/<int:id>')
def del_user(id):

    user=User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

# Route to get the list of all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  # Query all users from the database
    user_list = [{"id": user.id, "name": user.name, "phone_no": user.phone_no, "email": user.email} for user in users]
    return jsonify({"users": user_list})

@app.route("/add-user")
def createuser():
    return render_template("create.html")



# Route to update a user
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    # Fetch the user from the database by ID
    user = User.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        # Update the user's details with the new data from the form
        user.name = request.form.get("name")
        user.phone_no = request.form.get("phone_no")
        user.email = request.form.get("email")
        
        
        db.session.commit()  
        return redirect('/')
    return render_template('update.html', user=user)


# Home route
@app.route("/")
def hello_world():
    users = User.query.all()  # Get all users for displaying
    return render_template('index.html', users=users)

# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=8000)
