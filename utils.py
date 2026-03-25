def is_user_verified(custom_verify, enterprise_verify_reason):
  if not custom_verify and not enterprise_verify_reason:
    return False
  else:
    return True

def extract_follower_following(i):
  if not i:
    return None
  
  data = {
    'uid': i.get('uid'),
    'sec_uid': i.get('sec_uid'),
    'unique_id': i.get('unique_id'),
    'nickname': i.get('nickname'),
    'bio': i.get('signature'),
    'avatar': i.get('avatar_larger').url_list[0]
      if len(i.get('avatar_larger').url_list) > 0
      else '',
    'verified': is_user_verified(i.get('custom_verify'), i.get('enterprise_verify_reason')),
    'region': i.get('region'),
    'language': i.get('language'),
    'secret': i.get('secret'),
    'video_count': i.get('aweme_count'),
    'total_favorited': i.get('total_favorited'),
    'favoriting_count': i.get('favoriting_count'),
    'follower_count': i.get('follower_count'),
    'following_count': i.get('following_count'),
    'create_time': i.get('create_time'),
    'unique_id_modify_time': i.get('unique_id_modify_time')
  }

  return data
