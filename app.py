from flask import Flask, render_template, request

import pickle
import json
import mysql.connector

# -----------------------------------
# INITIALIZE FLASK APP
# -----------------------------------

app = Flask(__name__)

# -----------------------------------
# LOAD TRAINED ML MODEL
# -----------------------------------

with open("chatbot_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# -----------------------------------
# LOAD VECTORIZER
# -----------------------------------

with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# -----------------------------------
# LOAD CHATBOT RESPONSES
# -----------------------------------

with open("intents.json", "r") as file:
    responses = json.load(file)

# -----------------------------------
# CONNECT TO MYSQL DATABASE
# -----------------------------------

connection = mysql.connector.connect(

    host="localhost",

    user="root",

    password="Ateeb@30",

    database="ecommerce_chatbot"
)

cursor = connection.cursor()

# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/", methods=["GET", "POST"])

def home():

    user_message = ""
    bot_response = ""

    if request.method == "POST":

        # Get message from user
        user_message = request.form["message"]

        # Convert text into vector
        message_vector = vectorizer.transform([user_message])

        # Predict intent
        predicted_intent = model.predict(message_vector)[0]

        # Default chatbot response
        bot_response = responses.get(

            predicted_intent,

            "Sorry, I could not understand your query."
        )

        # -----------------------------------
        # ORDER TRACKING FEATURE
        # -----------------------------------

        if predicted_intent == "order_tracking":

            # Split sentence into words
            words = user_message.split()

            order_id = None

            # Find numeric order ID
            for word in words:

                if word.isdigit():

                    order_id = int(word)

                    break

            # If no order ID found
            if order_id is None:

                bot_response = "Please provide your order ID."

            else:

                # Fetch specific order
                sql = "SELECT * FROM orders WHERE order_id = %s"

                values = (order_id,)

                cursor.execute(sql, values)

                order = cursor.fetchone()

                # If order exists
                if order:

                    bot_response = (

                        f"Order ID: {order[0]} | "

                        f"Customer: {order[1]} | "

                        f"Status: {order[2]}"
                    )

                else:

                    bot_response = "Order not found."

        # -----------------------------------
        # STORE COMPLAINTS
        # -----------------------------------

        if (

    predicted_intent == "refund_request"

    or "refund" in user_message.lower()

):

            complaint_sql = """

            INSERT INTO complaints
            (customer_message, predicted_intent)

            VALUES (%s, %s)

            """

            complaint_values = (

                user_message,

                predicted_intent
            )

            cursor.execute(

                complaint_sql,

                complaint_values
            )

            connection.commit()

        # -----------------------------------
        # STORE CHAT HISTORY
        # -----------------------------------

        chat_sql = """

        INSERT INTO chat_history
        (user_message, bot_response)

        VALUES (%s, %s)

        """

        chat_values = (

            user_message,

            bot_response
        )

        cursor.execute(

            chat_sql,

            chat_values
        )

        connection.commit()

    return render_template(

        "index.html",

        user_message=user_message,

        bot_response=bot_response
    )

# -----------------------------------
# RUN FLASK APP
# -----------------------------------

if __name__ == "__main__":

    app.run(debug=True)