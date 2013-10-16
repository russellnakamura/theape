
# this package
from arachneape.commoncode.baseclass import BaseClass
from arachneape.components.countdown.countdown import CountDown
from arachneape.commoncode.strings import RESET, BLUE
from arachneape.commoncode.strings import BOLD, BOLD_THING, RED

# this module
from theoperator import OperatorError


BOLD_RED_MESSAGE = '{bold}{red}{{message}}{reset}'.format(bold=BOLD,
                                                          red=RED,
                                                          reset=RESET)
STAR = '*'
STARS = STAR * 5


class TheHortator(BaseClass):
    """
    An Exhorter of Operations
    """
    def __init__(self, operations, countdown=None):
        """
        TheHortator Constructor

        :param:

         - `operations`: iterable collection of Operators
         - `countdown`: CountDown timer
        """
        super(TheHortator, self).__init__()
        self.operations = operations
        self._countdown = countdown        
        return

    @property
    def countdown(self):
        """
        A Countdown Timer
        """
        if self._countdown is None:
            self._countdown = CountDown(iterations=len(self.operations))
        return self._countdown

    def __call__(self):
        """
        The main interface -- starts operations
        """
        self.countdown.start()
        count_string = "{b}** Operation {{c}} of {{t}} ('{{o}}') **{r}".format(b=BOLD, r=RESET)

        remaining_string = BOLD_THING.format(thing="Estimated Time Remaining:")
        total_elapsed = BOLD_THING.format(thing='** Total Elapsed Time:')
        
        total_count = len(self.operations)
        self.logger.info("{b}*** Starting Operations ***{r}".format(b=BOLD, r=RESET))
        
        for count, operation in enumerate(self.operations):
            if not self.countdown.time_remaining:
                self.logger.info('Time Exceeded, quitting')
                break

            self.logger.info(count_string.format(c=count+1,
                                                 t=total_count, o=str(operation)))
            self.logger.info(remaining_string.format(value=self.countdown.remaining))

            try:
                operation()
            except OperatorError as error:
                message = STARS + ' Operator Crash ' + STARS
                self.logger.error(BOLD_RED_MESSAGE.format(message=message))
                self.logger.error(error)
                self.logger.error(BOLD_RED_MESSAGE.format(message = STAR * len(message)))
            self.countdown.next_iteration()
        self.logger.info("{b}*** Ending Operations ***{r}".format(b=BOLD, r=RESET))
        self.logger.info(total_elapsed.format(value=self.countdown.elapsed))
        
        return
# end TheHortator
