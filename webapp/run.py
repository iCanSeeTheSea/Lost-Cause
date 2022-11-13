from app import app

if __name__ == '__main__':
    # host app on default ip
    app.run(host='0.0.0.0', port=8080)
