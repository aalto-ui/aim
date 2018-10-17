import os
import tornado.ioloop
import tornado.web
import handlers.metric_ws_handler
from tornado.options import define, options, parse_command_line, parse_config_file
import motor


define("environment", default=None, help="Runtime environment", type=str)
define("port", default=None, help="Port to listen on", type=int)
define("name", default=None, help="Instance name", type=str)
define("chrome_path", default=None, help="Path to Chrome executable", type=str)
define("layout_learning_path", default=None, help="Path to Layout Learning executable", type=str)
define("database_uri", default=None, help="Database URI", type=str)
define("results_data_dir", default=None, help="Directory to store result files", type=str)
define("screenshots_data_dir", default=None, help="Directory to store screenshot files", type=str)

def make_app():
    client = motor.motor_tornado.MotorClient(options.database_uri)
    db = client.get_database()
    return tornado.web.Application([
        (r"/metric", handlers.metric_ws_handler.MetricWebSocket),
    ], db=db, websocket_max_message_size=5767168) # 5.5 MB

def create_vg2_input_file(name):
    content = "\n".join([
        "layout1 configs/vg2_" + name + ".json",
        "layout2 configs/vg2_" + name + ".json",
        "screen-x 1280",
        "screen-y 720",
        "learning-time 6000",
        "swap-time 600",
        "n-runs 1",
        "output outputs/vg2_" + name + ".csv",
        "bla 6",
        "f 1.06",
        "fa 1.53",
        "fn 0.6",
        "ua 0.10",
        "us 0.30",
        "sa 3",
        "vstm 45",
        "eyes-start 110 0",
        "user-distance 1920",
        "no-learning t"
    ])
    with open("inputs/vg2_" + name + ".txt", "w") as f:
        f.write(content)

def main():
    # Determine execution environment and parse configs
    environment = os.environ.get("AIM_ENV", "development")
    if environment == "production":
        config_file = "configs/production.conf"
    elif environment == "test":
        config_file = "configs/test.conf"
    else:
        config_file = "configs/development.conf"
    parse_config_file(config_file)
    parse_command_line()

    app = make_app()
    app.listen(options.port)
    print("Execution environment: {}".format(options.environment))
    print("Server is listening on http://127.0.0.1:{}".format(options.port))
    print("Instance name: {}".format(options.name))
    print("Current working directory: {}".format(os.getcwd()))
    print("Chrome path: {}".format(options.chrome_path))
    print("Layout Learning path: {}".format(options.layout_learning_path))
    print("Database URI: {}".format(options.database_uri))
    create_vg2_input_file(options.name)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
