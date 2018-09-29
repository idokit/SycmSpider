import datetime
import logging
import sys

from sycm.util.Info import Info

logger = logging.getLogger(__name__)
from sycm.exception.error import LackOfDataException, SycmBusyException, SessionExpiredException


def handle(func):
    def wrapper(self, *args, **kw):
        try:
            func(self, *args, **kw)
        except Exception as e1:
            # 检查异常类型
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
                Info.send_info('{} message: {}'.format(self.driver.current_url, str(e)))
                sys.exit()
            except Exception as e:
                logger.error(self.driver.current_url + str(e))
                raise e1

    return wrapper
