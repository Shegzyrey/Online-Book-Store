from src import create_app


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from src.routes import start_consuming
        start_consuming()
