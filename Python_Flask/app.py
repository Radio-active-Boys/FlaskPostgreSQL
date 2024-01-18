from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

DB_HOST = "localhost"
DB_NAME = "School"
DB_USER = "postgres"
DB_PASS = "postgres"

db = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        try:
            cur = db.cursor()
            cur.execute("SELECT * FROM Students")
            students = cur.fetchall()
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            cur.close()
            return render_template("index.html", Students=students)   

@app.route("/insert", methods=["POST"])
def insert_data():
    if request.method == "POST":
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            print(name, email, phone)

            # Use db.cursor() instead of db.connection.cursor()
            cur = db.cursor()
            cur.execute("INSERT INTO Students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
            db.commit()
            
            # Your existing code
        except Exception as e:
            # Rollback the transaction
            db.rollback()
            print(f"Error: {e}")
        finally:
            # Close the cursor
            cur.close()
            flash('Student Added successfully')
            return redirect(url_for('index'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = db.cursor()  # Use db.cursor() instead of db.connection.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        db.commit()
        cur.close()
        return redirect(url_for('index'))


@app.route("/delete/<int:student_id>", methods=["GET"])
def delete_data(student_id):
    try:
        cur = db.cursor()
        cur.execute("DELETE FROM Students WHERE id = %s", (student_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        flash('Student Deleted successfully')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)