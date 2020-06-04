# /usr/bin/python
# coding=utf-8


class JokeCommentBean:

    def create_joke_comment_bean(self,
                         id,
                         joke_id,
                         article_id,
                         comment_user_id,
                         comment_user_img,
                         comment_user_nick_name,
                         comment_user_gender,
                         comment_user_age,
                         comment_user_content,
                         comment_type):

        bean = {'id': id,
                'joke_id': joke_id,
                'article_id': article_id,
                'comment_user_id': comment_user_id,
                'comment_user_img': comment_user_img,
                'comment_user_nick_name': comment_user_nick_name,
                'comment_user_gender': comment_user_gender,
                'comment_user_age': comment_user_age,
                'comment_user_content': comment_user_content,
                'comment_type': comment_type}
        return bean
