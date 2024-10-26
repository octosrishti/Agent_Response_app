from app import db, Message, app  # Ensure you import 'app'

# Use the correct app context
with app.app_context():
    messages = Message.query.all()
    for message in messages:
        print(f"ID: {message.id}, Customer: {message.customer_name}, Message: {message.message_content}")

