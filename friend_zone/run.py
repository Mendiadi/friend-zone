from friend_zone.server.routes import app, configure



if __name__ == '__main__':
    app.run(debug=True, host=configure.app_config.net_host, port=configure.app_config.port)