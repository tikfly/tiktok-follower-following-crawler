import csv
import asyncio
from tikfly import TikflyApi
from utils import extract_follower_following

X_API_KEY = 'YOUR_API_KEY' # Your API key used to authenticate requests to the Tikfly API. Get it from the official docs: https://docs.tikfly.io/getting-started/quickstart
UNIQUE_UD = 'khaby.lame' # Tiktok username of the target account
TYPE = 'following' # Specifies which user list to fetch: following or follower
COUNT = 5000 # The maximum number of users to retrieve

async def crawl():
  print('🏁 Start crawling...')
  tiktok = TikflyApi(X_API_KEY)

  try:
    user = await tiktok.get_user_info(UNIQUE_UD)
  except Exception as err:
    print(err)
    return

  user_sec_uid = (
    getattr(user, 'userInfo', None) and
    getattr(user.userInfo, 'user', None) and
    getattr(user.userInfo.user, 'secUid', None)
  )
  if not user_sec_uid:
    print(f'🚨 User {UNIQUE_UD} not found')
    return
  
  results = []
  max_time = 0
  
  while len(results) < COUNT:
    print(f'🚀 Crawling {user_sec_uid} (max_time={max_time}, total={len(results)})')
    try:
      res = await (
        tiktok.get_user_following(user_sec_uid, max_time=max_time)
        if TYPE == 'following'
        else tiktok.get_user_followers(user_sec_uid, max_time=max_time)
      )
    except Exception as err:
      print(err)
      break
    
    users = getattr(res, 'followers', None) or getattr(res, 'followings', None)
    has_more = getattr(res, 'has_more', False)
    max_time = getattr(res, 'max_time', 0)

    if users:
      for user in users:
        user = vars(user)
        user_ext = extract_follower_following(user)
        results.append(user_ext)
    
    if not users or not has_more or max_time == 0:
      print('⛓️‍💥 Stop loop: no more data')
      break
    
  if results:
    filename = f'{UNIQUE_UD}_{TYPE}.csv'
    fieldnames = list(results[0].keys())

    with open(filename, 'w', newline='', encoding='utf-8') as f:
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(results)

    print(f'✅ Saved {len(results)} records to {filename}')
  else:
    print('⚠️ No data to write')

if __name__ == '__main__':
  asyncio.run(crawl())
