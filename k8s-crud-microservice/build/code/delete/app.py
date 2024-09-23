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
logger = logging.getLogger("delete Module")
logger.setLevel(logging.DEBUG)

#create filehandler for logging
# Create a formatter with IST time
class ISTFileFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ist_timezone = pytz.timezone('Asia/Kolkata')  # IST timezone
        ist_datetime = datetime.datetime.now(ist_timezone)
        return ist_datetime.strftime("%Y_%m_%d_%H_%M_%S_IST")
fileformatter = ISTFileFormatter('%(asctime)s - delete Module - %(levelname)s - %(message)s')

current_datetime = datetime.datetime.now(pytz.utc)
ist_timezone = pytz.timezone('Asia/Kolkata')
ist_datetime = datetime.datetime.now(ist_timezone)
suffix = ist_datetime.strftime("_%Y_%m_%d_%H_%M_%S_IST")
code_execution_log_file = f"delete_module_{suffix}.log"
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

app = Flask("crud_delete_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")

home_service_url = os.environ.get("home_service_url")
read_service_url = os.environ.get("read_service_url")
delete_service_url = os.environ.get("delete_service_url")
create_service_url = os.environ.get("create_service_url")

@app.route("/form",methods=['POST','GET'])
def form():
    logger.info(f"The Create container name is {create_service_url}")
    logger.info(f"The Read container name is {read_service_url}")
    logger.info(f"The Redis hostname is {redis_host}")
    logger.info(f"The Redis host is {redis_host}")
    logger.info(f"The Home container is {home_service_url}")
    return render_template("form.html",delete_service_url=delete_service_url,home_service_url=home_service_url)

@app.route('/delete', methods=['POST'])
def delete():
    logger.info(f"The Create container name is {create_service_url}")
    logger.info(f"The Read container name is {read_service_url}")
    logger.info(f"The Redis hostname is {redis_host}")
    logger.info(f"The Redis host is {redis_host}")
    logger.info(f"The Home container is {home_service_url}")
    name =  request.form.get("delete_employee_name")
    logger.info(f"The User is {name}")
    delete_key= request.form.get("delete_key")
    logger.info(f"The Delete Key is {delete_key}")
    check_name=redis.hget(f"user:{name}","name")
    logger.info(f"The Name check from Redis is {check_name}")
    if check_name!=None:
      logger.info(f"The User exists in Redis")
      if delete_key=="delete_employee_id":
          delete_key="Employee ID"
          redis.hdel(f"user:{name}","id")
      elif delete_key=="delete_employee_mail":
          delete_key="Employee Mail"
          redis.hdel(f"user:{name}","email")
      elif delete_key=="delete_user":
          delete_key="User"
          redis.delete(f"user:{name}")
      else:
        return "No Key is submitted to delete"
      return render_template("delete.html",delete_key=delete_key,employee_name=name,home_service_url=home_service_url,read_service_url=read_service_url)
    else:
      logger.error(f"The User doesnt exists..Kindly check the Username once")
      return render_template("error.html",name=name,read_service_url=read_service_url,create_service_url=create_service_url,home_service_url=home_service_url)
    

if __name__ == "__main__":
    port=os.environ.get("delete_port")
    app.run(debug=True, host="0.0.0.0")

