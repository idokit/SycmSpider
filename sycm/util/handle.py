import datetime
import logging
import sys

from sycm.lib.Info import Info
logger = logging.getLogger(__name__)
from sycm.exception.error import LackOfDataException,SycmBusyException,SessionExpiredException

def handle(func):
    def wrapper(self, *args, **kw):
        try:
            func(self, *args, **kw)
        except Exception as e:
            # 检查异常类型
            logger.error(e)
            try:
                self.check_error()
            except LackOfDataException as e:
                logger.error(e)
                return
            except SycmBusyException as e:
                logger.error(e)
                self.driver.refresh()
                return func(self, *args, **kw)
            except SessionExpiredException as e:
                logger.error(self.driver.current_url + str(e))
                Info.send_info('{}message:{}' .format (self.driver.current_url, str(e)))
                sys.exit()
            except Exception as e:
                Info.send_info('{}message:{}' .format (self.driver.current_url, str(e)))
                raise e

            raise e
            # self.get_screenshot_as_file(
            #     'img/%s.png' % str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
    return wrapper










