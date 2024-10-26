import pandas as pd
from models import db, Message
from app import app

def load_messages_from_csv(csv_path):
    data = pd.read_csv(csv_path)
    with app.app_context():
        for _, row in data.iterrows():
            message = Message(
                customer_name=row['customer_name'],
                message=row['message'],
                urgent=row['urgent'].lower() == 'true'
            )
            db.session.add(message)
        db.session.commit()

if __name__ == '__main__':
    load_messages_from_csv('messages.csv')
