import instaloader
import pprint
import re

def banner():
    print('\t""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')
    print('\t                         Instagram Profile Data Grabber                    ')
    print('\t""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')

def is_valid_username(username):
    return re.match(r'^[\w.-]{1,30}$', username) is not None

def get_profile_data(username):
    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        instagram_profile = {
            'success': True,
            'profile': {
                'name': profile.full_name,
                'username': profile.username,
                'followers': profile.followers,
                'following': profile.followees,
                'posts': profile.mediacount,
                'bio': profile.biography,
                'profile_pic_url': profile.profile_pic_url,
                'external_url': profile.external_url,
                'is_private': profile.is_private,
                'is_verified': profile.is_verified,
                'igtv_count': profile.igtvcount,
                'has_highlight_reels': profile.has_highlight_reels,
                'business_category': profile.business_category_name,
                'followers_list': None,  # Placeholder for followers list
                'following_list': None,  # Placeholder for following list
                'story_highlights': None  # Placeholder for story highlights
            }
        }

        # Attempt to access followers and following lists
        if not profile.is_private:
            instagram_profile['profile']['followers_list'] = [f.username for f in profile.get_followers()]
            instagram_profile['profile']['following_list'] = [f.username for f in profile.get_followees()]
            instagram_profile['profile']['story_highlights'] = [{'title': hl.title, 'cover_url': hl.cover_url} for hl in profile.get_highlight_posts()]

            # Recent posts
            instagram_profile['recent_posts'] = []
            total_likes = 0
            total_comments = 0

            for post in profile.get_posts():
                if len(instagram_profile['recent_posts']) >= 5:
                    break
                post_info = {
                    'caption': post.caption,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/",
                    'likes': post.likes,
                    'comments': post.comments,
                    'timestamp': post.date_utc.isoformat(),
                    'location': post.location.name if post.location else None,
                    'comments_data': [{'user': comment.owner.username, 'text': comment.text} for comment in post.get_comments()]
                }
                total_likes += post.likes
                total_comments += post.comments
                instagram_profile['recent_posts'].append(post_info)

            # Engagement rate
            if profile.followers > 0:
                engagement_rate = (total_likes + total_comments) / profile.followers
                instagram_profile['engagement_rate'] = engagement_rate

        else:
            # If the profile is private, note that followers and following lists are inaccessible
            instagram_profile['profile']['followers_list'] = {'error': "Profile is private."}
            instagram_profile['profile']['following_list'] = {'error': "Profile is private."}
            instagram_profile['profile']['story_highlights'] = {'error': "Profile is private."}

        return instagram_profile

    except instaloader.exceptions.ProfileNotExistsException:
        return {'success': False, 'error': f"Profile {username} does not exist"}
    except instaloader.exceptions.LoginRequiredException:
        return {'success': False, 'error': "Login required to access followers and following lists."}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def download_profile_picture(username):
    L = instaloader.Instaloader()

    try:
        L.download_profile(username, profile_pic_only=True)
        print("Profile picture downloaded successfully.")
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile {username} does not exist.")
    except Exception as e:
        print(f"Error occurred while downloading the profile picture: {str(e)}")

def download_recent_posts(username, post_count=5):
    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        print(f"\nDownloading {post_count} recent posts from {username}:")
        for post in profile.get_posts():
            if post_count == 0:
                break
            L.download_post(post, target=profile.username)
            post_count -= 1

        print("Recent posts downloaded successfully.")

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile {username} does not exist.")
    except Exception as e:
        print(f"Error occurred while downloading recent posts: {str(e)}")

# Main function to grab Instagram profile data, download profile picture, and recent posts
if __name__ == "__main__":
    username = input("Enter Instagram username: ")
    banner()

    if is_valid_username(username):
        profile_data = get_profile_data(username)
        pprint.pprint(profile_data)

        if profile_data['success']:
            download_profile_picture(username)
            download_recent_posts(username, post_count=5)
    else:
        print("Invalid Instagram username format.")
