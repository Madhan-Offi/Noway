import time
import cloudscraper
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# eg: https://gplinks.co/XXXX
url = ""

# gplink url
def link_handler(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        link = args[1]
    else:
        link = ''
    try:
      is_gplink = True if "droplink" in link else False
      if is_gplink:
          msg = sendMessage(f'𝗕𝘆𝗽𝗮𝘀𝘀𝗶𝗻𝗴 𝘆𝗼𝘂𝗿 𝗚𝗽𝗹𝗶𝗻𝗸 𝗟𝗶𝗻𝗸: <code>{link}</code>\n\n𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩 𝙖 𝙢𝙞𝙣𝙪𝙩𝙚.', context.bot, update)
          baashax = gplinks_bypass(link)
          links = baashax.get('url')
          deleteMessage(context.bot, msg)
          bx = sendMessage(f"𝙄'𝙫𝙚 𝙎𝙚𝙣𝙙 𝙩𝙝𝙚 𝘽𝙮𝙥𝙖𝙨𝙨𝙚𝙙 𝙇𝙞𝙣𝙠 𝙩𝙤 𝙮𝙤𝙪𝙧 𝙋𝙈.", context.bot, update)
          sendPrivate(f'𝗚𝗶𝘃𝗲𝗻 𝗟𝗶𝗻𝗸: <code>{link}</code>\n\n𝗕𝘆𝗽𝗮𝘀𝘀𝗲𝗱 𝗟𝗶𝗻𝗸: <code>{links}</code>', context.bot, update)
      else:
          sendMessage('𝗦𝗲𝗻𝗱 𝗚𝗽𝗹𝗶𝗻𝗸 𝗟𝗶𝗻𝗸𝘀 𝗮𝗹𝗼𝗻𝗴 𝘄𝗶𝘁𝗵 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.', context.bot, update)
    except DDLException as e:
        LOGGER.error(e)

# =======================================

def gplinks_bypass(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/','/')
    except: return 'Something went wrong :('

# =======================================

print(gplinks_bypass(url))

gplink_handler = CommandHandler(BotCommands.GpCommand, link_handler,
dispatcher.add_handler(gplink_handler)

