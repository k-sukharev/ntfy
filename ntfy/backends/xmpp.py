import logging
import os

import slixmpp


class NtfySendMsgBot(slixmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, title, message, mtype=None):
        super().__init__(jid, password)

        self.recipient = recipient
        self.title = title
        self.msg = message
        self.mtype = mtype

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("connection_failed", self.on_connection_failed)

    def on_connection_failed(self, event):
        logging.getLogger(__name__).error('XMPP connection failed')
        self.disconnect(wait=0.0, reason='connection failed')

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        msg_args = {
            'mto': self.recipient,
            'msubject': self.title,
            'mbody': self.msg
        }
        if self.mtype:
            msg_args['mtype'] = self.mtype

        self.send_message(**msg_args)

        self.disconnect(wait=2.0)


def notify(title,
           message,
           jid=None,
           password=None,
           recipient=None,
           hostname=None,
           port=5222,
           path_to_certs=None,
           mtype=None,
           retcode=None):
    jid = jid or os.environ.get('NTFY_XMPP_USER')
    password = password or os.environ.get('NTFY_XMPP_PASSWORD')
    recipient = recipient or os.environ.get('NTFY_XMPP_RECIPIENT')

    if not all([jid, password, recipient]):
        raise ValueError(
            'jid, password, and recipient are required. '
            'Set via config or NTFY_XMPP_USER, NTFY_XMPP_PASSWORD, '
            'NTFY_XMPP_RECIPIENT environment variables.'
        )

    xmpp_bot = NtfySendMsgBot(jid, password, recipient, title, message, mtype)

    if path_to_certs and os.path.isdir(path_to_certs):
        xmpp_bot.ca_certs = path_to_certs

    if hostname:
        xmpp_bot.connect(host=hostname, port=int(port))
    else:
        xmpp_bot.connect()

    xmpp_bot.loop.run_until_complete(xmpp_bot.disconnected)
