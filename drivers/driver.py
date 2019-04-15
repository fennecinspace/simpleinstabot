from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, sys, subprocess
# logging
import logging
logger = logging.getLogger(__name__)

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

DEFAULT_ARGS = [
    '--headless',
    '--no-sandbox',
    '--disable-gpu',
    '--remote-debugin-port=9222',
    '--screen-size=1200x800',
]

DEFAULT_ARGS_EXPERIMENTAL = [{
    "prefs" : {
        "profile.default_content_settings.cookies": 2,
        "profile.default_content_settings.images": 2,
        "profile.managed_default_content_settings.images": 2,
        "disk-cache-size": 4096,
    } 
}]


def create_driver(driver_type = 'chrome', exec_path = None, args = DEFAULT_ARGS, args_experimental = DEFAULT_ARGS_EXPERIMENTAL, remote_version = False):
    '''
    return a selenium connected driver, make sure to have phantomjs or chrome installed before using them
    '''

    driver_type = driver_type.lower().strip()

    try:
        if remote_version:
            try:
                driver_options = webdriver.ChromeOptions()
                
                if args:
                    for arg in args:
                        driver_options.add_argument(arg)
                
                if args_experimental:
                    for arg in args_experimental:
                        key, value = list(arg.items())[0]
                        driver_options.add_experimental_option(key, value)

                driver = webdriver.Remote(command_executor = exec_path or 'http://selenium:4444/wd/hub', desired_capabilities = driver_options.to_capabilities())
                return driver

            except Exception as e:
                logger.error('Could Not Create Remote Driver')
                logger.exception(e)

        else:
            if 'chrome' in driver_type:
                chrome_path = [BASE_PATH, "chromedriver"]
                driver_options = webdriver.chrome.options.Options()
                
                if args:
                    for arg in args:
                        driver_options.add_argument(arg)
                
                if args_experimental:
                    for arg in args_experimental:
                        key, value = list(arg.items())[0]
                        driver_options.add_experimental_option(key, value)

                ## no images and cookies
                # driver_options.experimental_options['prefs'] = {
                #     "profile.default_content_settings.cookies": 2,
                #     "profile.default_content_settings.images": 2,
                #     "profile.managed_default_content_settings.images": 2,
                #     "disk-cache-size": 4096,
                # } 

                driver =  webdriver.Chrome(executable_path = exec_path or os.path.join(*chrome_path), chrome_options = driver_options)
                return driver

            if driver_type == 'phantomjs': ## deprectaed
                driver = webdriver.PhantomJS(executable_path = exec_path or subprocess.getoutput('which phantomjs'))
                return driver
                

            logger.error('Please Select A Valid Driver')
            return None

    except Exception as e:
        logger.error('Could Not Create Driver')
        logger.exception(e)
        return None