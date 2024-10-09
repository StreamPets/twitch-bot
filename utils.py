def to_ordinal(cardinal):
  if cardinal in [11, 12, 13]:
    return f'{cardinal}th'
  
  match (cardinal % 10):
    case 1: return f'{cardinal}st'
    case 2: return f'{cardinal}nd'
    case 3: return f'{cardinal}rd'
    case _: return f'{cardinal}th'

def format_sse(data: str, event=None) -> str:
  msg = f'data: {data}\n\n'
  if event is not None:
    msg = f'event: {event}\n{msg}'
  return msg

BOT_NAMES = ['rexxauto', 'streamelements']
CHANNEL_NAME = 'LJRexCodes'
