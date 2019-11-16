import instaloader, jdatetime
from abc import ABCMeta, abstractmethod

class Main(metaclass = ABCMeta):

    @abstractmethod
    def get_info(self):
        pass

class Child(Main):

    def __init__(self, username):

        self.L = instaloader.Instaloader()
        self.profile = instaloader.Profile.from_username(self.L.context, username)

    def get_info(self):

        answer = {}

        ## calculate engagment and view_engagment
        all_comments_likes = self.get_count_likes_and_comments()

        engagment = (((all_comments_likes['count_likes'] / self.get_posts_count()) + (all_comments_likes['count_comments'] / self.get_posts_count())) / self.get_followrs_count()) * 100
        view_engagment = (((all_comments_likes['count_likes_video'] / self.get_posts_count()) + (all_comments_likes['count_comments_video'] / self.get_posts_count())) / self.get_followrs_count()) * 100

        ## calculate fake followers
        if engagment >= 1:
            fake_followers = "ندارد"
            real_followers = self.get_followrs_count()
        else:
            fake_followers = self.get_followrs_count() * engagment
            real_followers = round(self.get_followrs_count() - round(fake_followers))

        ## calculate mean like, comments, view
        mean_like = all_comments_likes['count_likes'] / self.get_posts_count()
        mean_comment = all_comments_likes['count_comments'] / self.get_posts_count()
        mean_view =  all_comments_likes['view_video'] / self.get_posts_count()
        
        if all_comments_likes['video_count']:
            
            avg_video_like = round(all_comments_likes['count_likes_video']/all_comments_likes['video_count'])
            avg_video_comment = round(all_comments_likes['count_comments_video']/all_comments_likes['video_count'])
            
        else:
            avg_video_like = 0
            avg_video_comment = 0

        answer.update({'username':self.profile.username,
                       'engagment':engagment,
                       'view_engagment':view_engagment,
                       'fake_followers':fake_followers,
                       'real_followers':real_followers,
                       'following':self.get_followees_count(),
                       'followers':self.get_followrs_count(),
                       "avg_like":round(mean_like),
                       "avg_video_like":avg_video_like,
                       "avg_comment":round(mean_comment),
                       "avg_video_comment":avg_video_comment,
                       "agv_view":round(mean_view),
                       'num_posts':self.get_posts_count(),
                       'user_id':self.profile.userid,
                       'avg_comment_like_ratio':mean_comment / mean_like,
                       'avg_like_follower_ratio':mean_like / self.get_followrs_count(),
                       'date': jdatetime.datetime.now(),
                       })

        return answer

    def get_followrs_count(self):
        return self.profile.followers

    def get_followees_count(self):
        return self.profile.followees

    def get_posts_count(self):
        return self.profile.mediacount

    def get_count_likes_and_comments(self):

        count_comments = 0
        count_likes = 0

        count_comments_video = 0
        count_likes_video = 0

        view_video = 0

        video_count = 0
        image_count = 0

        posts_generator = self.profile.get_posts()

        for p in posts_generator:
            x = p.__dict__['_node']
            # print(x)

            count_comments += x['edge_media_to_comment']['count']
            count_likes += x['edge_media_preview_like']['count']
            image_count += 1

            if x['__typename'] == 'GraphVideo':
                count_comments_video += x['edge_media_to_comment']['count']
                count_likes_video += x['edge_media_preview_like']['count']
                view_video += x['video_view_count']
                video_count += 1

        return {'count_comments':count_comments,
                'count_likes':count_likes,
                'count_comments_video' : count_comments_video,
                'count_likes_video':count_likes_video,
                'view_video':view_video,
                'video_count':video_count,
                'image_count':image_count}


