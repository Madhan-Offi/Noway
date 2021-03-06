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
          msg = sendMessage(f'ššš½š®ššš¶š»š“ šš¼ššæ šš½š¹š¶š»šø šš¶š»šø: <code>{link}</code>\n\nšš”šššØš š¬ššš© š š¢šš£šŖš©š.', context.bot, update)
          baashax = gplinks_bypass(link)
          links = baashax.get('url')
          deleteMessage(context.bot, msg)
          bx = sendMessage(f"š'š«š ššš£š š©šš š½š®š„ššØšØšš ššš£š  š©š¤ š®š¤šŖš§ šš.", context.bot, update)
          sendPrivate(f'šš¶šš²š» šš¶š»šø: <code>{link}</code>\n\nššš½š®ššš²š± šš¶š»šø: <code>{links}</code>', context.bot, update)
      else:
          sendMessage('š¦š²š»š± šš½š¹š¶š»šø šš¶š»šøš š®š¹š¼š»š“ šš¶ššµ š°š¼šŗšŗš®š»š±.', context.bot, update)
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

