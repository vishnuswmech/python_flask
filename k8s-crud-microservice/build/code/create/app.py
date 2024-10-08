from flask import Flask,render_template,request,jsonify
import os,redis
import logging
import datetime
import pytz
import glob
import traceback
file_pattern = '*.log'
current_directory = os.getcwd()

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    datefmt='%m/%d/%Y %I:%M:%S %p'
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,datefmt=self.datefmt)
        return formatter.format(record)
logger = logging.getLogger("Create-module")
logger.setLevel(logging.DEBUG)

#create filehandler for logging
# Create a formatter with IST time
class ISTFileFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ist_timezone = pytz.timezone('Asia/Kolkata')  # IST timezone
        ist_datetime = datetime.datetime.now(ist_timezone)
        return ist_datetime.strftime("%Y_%m_%d_%H_%M_%S_IST")
fileformatter = ISTFileFormatter('%(asctime)s - create-module - %(levelname)s - %(message)s')

current_datetime = datetime.datetime.now(pytz.utc)
ist_timezone = pytz.timezone('Asia/Kolkata')
ist_datetime = datetime.datetime.now(ist_timezone)
suffix = ist_datetime.strftime("_%Y_%m_%d_%H_%M_%S_IST")
code_execution_log_file = f"create_module_{suffix}.log"
error_execution_log_file = f"{code_execution_log_file}"

for file_path in glob.glob(os.path.join(current_directory, file_pattern)):
    try:
        logger.info("Removing .log file files")
        os.remove(file_path)
        logger.info(".log files were removed successfully")

    except OSError:
        logger.info(".log files doesnot exist, so passing...")
        pass



filehandler = logging.FileHandler(code_execution_log_file)

filehandler.rotation = "100 MB"
logger.addHandler(filehandler)
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(fileformatter)


# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

#IST timezone suffix
current_datetime = datetime.datetime.now(pytz.utc)
ist_timezone = pytz.timezone('Asia/Kolkata')
ist_datetime = datetime.datetime.now(ist_timezone)
suffix = ist_datetime.strftime("_%Y_%m_%d_%H_%M_%S_IST")


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log the exception using traceback
            logging.error("An error occurred in %s: %s", func.__name__, traceback.format_exc())
            logger.info(f"The log file name is {error_execution_log_file} and bucket is {s3_bucket}")
            # Upload the error log file to S3
            send_to_s3(error_execution_log_file, s3_bucket)

            # Re-raise the exception to maintain program flow
            raise

    return wrapper


app = Flask("crud_create_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")
read_service_url = os.environ.get("read_service_url")
create_service_url=os.environ.get("create_service_url")
home_service_url=os.environ.get("home_service_url")
update_service_url=os.environ.get("update_service_url")


@app.route("/form",methods=["POST","GET"])
def form():
    logger.info(f"The Create service URL is {create_service_url}")
    logger.info(f"The Read service URL is {read_service_url}")
    logger.info(f"The Update service URL is {update_service_url}")
    return render_template("form.html",create_service_url=create_service_url,home_service_url=home_service_url)

@app.route('/create', methods=['POST'])
def create():
    name =  request.form.get("employee_name")
    employee_id= request.form.get("employee_id")
    employee_mail = request.form.get("employee_mail")
    logger.info(f"The Create service URL is {create_service_url}")
    logger.info(f"The Read service URL is {read_service_url}")
    logger.info(f"The Update service URL is {update_service_url}")
    check_name=redis.hget(f"user:{name}","name")
    logger.info(f"The Employee name is {name}")
    logger.info(f"The Employee ID is {employee_id}")
    logger.info(f"The Employee Mail is {employee_mail}")
    logger.info(f"The Name check from Redis is {check_name}")
    if check_name==None:
      logger.info(f"The Name check is None, so,creating New entry")
      redis.hset(f"user:{name}", mapping={"name": f"{name}", "id": f"{employee_id}", "email": f"{employee_mail}"})
      return render_template("create.html",employee_id=employee_id,employee_mail=employee_mail,employee_name=name,home_service_url=home_service_url,read_service_url=read_service_url)
    else:
      logger.error(f"The name {name} already exists, kindly check the name once and use Update portal to update the details for existing users.")
      return render_template("error.html",employee_id=employee_id,employee_mail=employee_mail,employee_name=name,update_service_url=update_service_url,home_service_url=home_service_url,create_service_url=create_service_url)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200
      

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
