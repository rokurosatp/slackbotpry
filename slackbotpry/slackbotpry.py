"""Main Module
Slack RTM APIのイベント処理により動作するbotを起動する
"""
import sys
import argparse

def make_argparser():
    """Create Command Line Parser
    DESCRIPTION:
        This function creates ArgumentParser Object and make arguments for this app.
    NOTE:
        今後の拡張性のためにArgumentParserオブジェクトでコマンドラインのパースをしていますが今のところ
        python slackbotpry APITOKEN
        ってだけです
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", "-c", default="random", help='channel to post message')
    parser.add_argument("APITOKEN", type=str, help='api token for slack bot/integration you use')
    return parser
def main():
    """Main Routine
    PROCESS:
        1.analyze commandline
        2.get api_token
        3.post to slack
    """
    import bot
    # parse commandline arguments
    argparser = make_argparser()
    argument = argparser.parse_args()
    # get api token
    api_token = argument.APITOKEN
    mybot = bot.Bot(api_token, argument.channel)
    from eventhandler import SimpleMessageHandler
    def chat_callback(**kw):
        return 'Hi!'
    def edit_callback(handler, event, text):
        if handler.last_post:
            event.bot.edit_message(text, handler.last_post)
    mybot.post_message('Hi')
    mybot.add_eventhandler(SimpleMessageHandler(r'^Hello', chat_callback, edit_callback))
    mybot.add_eventhandler(SimpleMessageHandler(r'^good$', lambda event, **kw: event.add_reaction('+1')))
    mybot.mainloop()
if __name__ == "__main__":
    main()
