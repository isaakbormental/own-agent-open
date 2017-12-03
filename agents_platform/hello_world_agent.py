import json
import re
import threading
import time
import traceback

import websocket

import logger
from own_adapter.agent import Agent
from own_adapter.board import Board
from own_adapter.element import Element
from own_adapter.platform_access import PlatformAccess

AGENT_LOGIN = 'bisensualagent@gmail.com'
AGENT_PASSWORD = 'bisensualagent1'


def __do_something(element):
    """Write your code here"""

    # examples:
    # put a message to a board
    message = 'I am the best bot EVER!!!!'
    #print('fwe'+element.get_name())
    element.get_board().put_message(message)

    # put a URL to an element
    url = 'https://www.own.space/'
    element.put_link(url)


def __run_on_element(element):
    """Running on a target element"""
    try:
        __do_something(element)
    except Exception as ex:
        logger.exception('helloworld', 'Error: could not process an element. Element id: {}. Exception message: {}.\n'
                                       '{}'.format(element.get_id(), str(ex), traceback.format_exc()))


def __run_on_board(board):
    """Runs the agent on elements of a board"""
    elements = board.get_elements()
    for element in elements:
        __run_on_element(element)


def periodical_update():
    """Does periodical work with a predefined time interval"""
    time_interval = 86400

    while (True):

        agent = get_agent()
        boards = agent.get_boards()

        for board in boards:
            if board.get_id() == '101':
                board.add_element(3, 3, 3, 5, 'First report')
                board.add_element(1, 4, 2, 3, 'Second report')
                board.add_element(6, 4, 2, 3, 'Third report')
                board.add_element(4, 1, 1, 2, 'Fourth report')
                board.add_element(4, 8, 1, 2, 'Fifth report')
                board.add_element(2, 2, 1, 1, 'Sixth report')
                board.add_element(6, 2, 1, 1, 'Seventh report')
                board.add_element(2, 8, 1, 1, 'Eighth report')
                board.add_element(6, 8, 1, 1, 'Ninth report')

                for element in board.get_elements():
                    time.sleep(10)
                    # print(element.get_url())
                    if element.get_name() == 'First report':
                        with open('1.pdf', 'rb') as f1:
                            file_bytes = bytearray(f1.read())
                            element.put_file('1.pdf', file_bytes)

                    if element.get_name == 'Second report':
                        with open('2.pdf', 'rb') as f2:
                            file_bytes = bytearray(f2.read())
                            element.put_file('2.pdf', file_bytes)

                    if element.get_name == 'Third report':
                        with open('3.pdf', 'rb') as f3:
                            file_bytes = bytearray(f3.read())
                            element.put_file('3.pdf', file_bytes)

                    if element.get_name == 'Fourth report':
                        with open('4.pdf', 'rb') as f4:
                            file_bytes = bytearray(f4.read())
                            element.put_file('4.pdf', file_bytes)

                    if element.get_name == 'Fifth report':
                        with open('5.pdf', 'rb') as f5:
                            file_bytes = bytearray(f5.read())
                            element.put_file('5.pdf', file_bytes)

                    if element.get_name == 'Sixth report':
                        with open('6.pdf', 'rb') as f6:
                            file_bytes = bytearray(f6.read())
                            element.put_file('6.pdf', file_bytes)

                    if element.get_name == 'Seventh report':
                        with open('7.pdf', 'rb') as f7:
                            file_bytes = bytearray(f7.read())
                            element.put_file('7.pdf', file_bytes)

                    if element.get_name == 'Eighth report':
                        with open('8.pdf', 'rb') as f8:
                            file_bytes = bytearray(f8.read())
                            element.put_file('8.pdf', file_bytes)

                    if element.get_name == 'Ninth report':
                        with open('9.pdf', 'rb') as f9:
                            file_bytes = bytearray(f9.read())
                            element.put_file('9.pdf', file_bytes)

                message = 'Following scientific research papers have been selected for you'
                board.put_message(message)




                # put a URL to an element
                # url = 'https://www.own.space/'
                # element.put_link(url)







                # def add_element(self, pos_x, pos_y, size_x=1, size_y=1, caption=''):

    time.sleep(time_interval)



def get_agent():
    """Returns the current agent"""
    login = AGENT_LOGIN
    password = AGENT_PASSWORD

    platform_access = PlatformAccess(login, password)
    helloworld_agent = Agent(platform_access)

    return helloworld_agent


def on_websocket_message(ws, message):
    """Processes websocket messages"""
    message_dict = json.loads(message)
    content_type = message_dict['contentType']
    message_type = content_type.replace('application/vnd.uberblik.', '')

    logger.debug('helloworld', message)
    # if message_type == 'liveUpdateActivityUpdated+json':
    if message_type == 'liveUpdateActivitiesUpdated+json':
        print('I heard live activity {0}'.format(message_dict))
        if message_dict['type'] == 'PostedToBoard':
            print('message detected')
            message_info = message_dict['displayText']
            print(message_info)

    if message_type == 'liveUpdateElementCaptionEdited+json':
        element_caption = message_dict['newCaption']
        # looking for elements that target our agent
        if re.match(pattern='@helloworld:.+', string=element_caption):
            # create instances of Board and Element to work with them
            element_id = message_dict['path']
            news_agent = get_agent()
            board_id = '/'.join(element_id.split('/')[:-2])
            board = Board.get_board_by_id(board_id, news_agent.get_platform_access(), need_name=False)
            element = Element.get_element_by_id(element_id, news_agent.get_platform_access(), board)
            if element is not None:
                __run_on_element(element)


def on_websocket_error(ws, error):
    """Logs websocket errors"""
    logger.error('helloworld', error)


def on_websocket_open(ws):
    """Logs websocket openings"""
    logger.info('helloworld', 'Websocket is open')


def on_websocket_close(ws):
    """Logs websocket closings"""
    logger.info('helloworld', 'Websocket is closed')


def open_websocket():
    """Opens a websocket to receive messages from the boards about events"""
    agent = get_agent()
    # getting the service url without protocol name
    platform_url_no_protocol = agent.get_platform_access().get_platform_url().split('://')[1]
    access_token = agent.get_platform_access().get_access_token()
    url = 'ws://{}/opensocket?token={}'.format(platform_url_no_protocol, access_token)

    ws = websocket.WebSocketApp(url,
                                on_message=on_websocket_message,
                                on_error=on_websocket_error,
                                on_open=on_websocket_open,
                                on_close=on_websocket_close)
    ws.run_forever()


def run():
    websocket_thread = None
    updater_thread = None

    while True:
        # opening a websocket for catching server messages
        if websocket_thread is None or not websocket_thread.is_alive():
            try:
                websocket_thread = threading.Thread(target=open_websocket)
                websocket_thread.start()
            except Exception as e:
                logger.exception('helloworld', 'Could not open a websocket. Exception message: {}'.format(str(e)))

        # periodical updates
        if updater_thread is None or not updater_thread.is_alive():
            try:
                updater_thread = threading.Thread(target=periodical_update)
                updater_thread.start()
            except Exception as e:
                logger.exception('helloworld', 'Could not start updater. Exception message: {}'.format(str(e)))

        # wait until next check
        time.sleep(10)


if __name__ == '__main__':
    run()
