from flask import Flask,render_template,request
import os
import logging
import datetime
import pytz
import glob
import traceback
file_pattern = '*.log'
current_directory = os.getcwd()
app = Flask("crud_home_app")

port=os.environ.get("home_port")
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
# create logger with 'sanity check application'
logger = logging.getLogger("Sanity Checks")
logger.setLevel(logging.DEBUG)

#create filehandler for logging
# Create a formatter with IST time
class ISTFileFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ist_timezone = pytz.timezone('Asia/Kolkata')  # IST timezone
        ist_datetime = datetime.datetime.now(ist_timezone)
        return ist_datetime.strftime("%Y_%m_%d_%H_%M_%S_IST")
fileformatter = ISTFileFormatter('%(asctime)s - sanity checks - %(levelname)s - %(message)s')

current_datetime = datetime.datetime.now(pytz.utc)
ist_timezone = pytz.timezone('Asia/Kolkata')
ist_datetime = datetime.datetime.now(ist_timezone)
suffix = ist_datetime.strftime("_%Y_%m_%d_%H_%M_%S_IST")
code_execution_log_file = f"infra_sanity_checks_{suffix}.log"
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


create_con_name=os.environ.get("create_con_name")
create_port=os.environ.get("create_port")
custom_network=os.environ.get("custom_network_name")
read_con_name=os.environ.get("read_con_name")
read_port=os.environ.get("read_port")
update_con_name=os.environ.get("update_con_name")
update_port=os.environ.get("update_port")
delete_con_name=os.environ.get("delete_con_name") 
delete_port=os.environ.get("delete_port")
@app.route("/")
def root():
    logger.info(f"The Create container name is {create_con_name}")
    logger.info(f"The Create module port is {create_port}")
    logger.info(f"The Custom docker network name is {custom_network}")
    logger.info(f"The Read container name is {read_con_name}")
    logger.info(f"The Read module port is {read_port}")
    logger.info(f"The Update container name is {update_con_name}")
    logger.info(f"The Update module port is {update_port}")
    logger.info(f"The Delete container name is {delete_con_name}")
    logger.info(f"The Delete module port is {delete_port}")
    return render_template("index.html",delete_con_name=delete_con_name,delete_port=delete_port,update_con_name=update_con_name,update_port=update_port,create_con_name=create_con_name,read_con_name=read_con_name,read_port=read_port,custom_network=custom_network,create_port=create_port)

port=os.environ.get("home_port")
app.run(debug=True,host="0.0.0.0",port=port)

