"""Main Module
起動したら投稿して終了する。
"""
import sys
import argparse
import slacker

def make_argparser():
    """Create Command Line Parser
    DESCRIPTION:
        This function creates ArgumentParser Object and make arguments for this app.
    NOTE:
        今後の拡張性のためにArgumentParserオブジェクトでコマンドラインのパースをしていますが今のところ
        python slackbotcommander APITOKEN
        ってだけです
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", help='channel to post message')
    parser.add_argument("APITOKEN", default="random", help='api token for slack bot/integration you use')
    return parser
def get_channel(slack: slacker.Slacker, channel_name: str):
    """get the channel_name for integration
    NOTE:一応DMや自分DM等の対応のための余地として作っといた
    """
    return channel_name
def main():
    """Main Routine
    PROCESS:
        1.analyze commandline
        2.get api_token
        3.post to slack
    """
    # parse commandline arguments
    argparser = make_argparser()
    argument = argparser.parse_args(sys.argv)
    # get api token
    api_token = argument.APITOKEN
    slack = slacker.Slacker(api_token)
    channel_id = get_channel(slack, argument.channel_name)
    slack.chat.post_message(channel_id, 'Hello!')
if __name__ == "__main__":
    main()
