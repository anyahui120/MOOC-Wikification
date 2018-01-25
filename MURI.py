#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Ann
# @Site    :
# @File    : MURI.py
# @Software: PyCharm

import os
import re
import sqlite3


class CreatePostTable(object):
    """This class is used for collecting posts data from original crawled data.

    In our database, posts are saved in posts and comments. Table thread contains the title of each thread.
    Posts are saved in one database nusdata.db. Resources are saved in MOOCDB.db

    Attributes:
        db_resource_path: the path of database that collecting resources.  # MOOCDB.db
        db_source_path: the path of database that collecting the original data.  #nusdata.db
        db_target_path: the path of database that saving the final designed post data.  #create one, if exist, delete and recreate
        dbs_path: C:\Users\anyah\OneDrive\Wikifier-master\Wikifier-master\server-master
    """

    def __init__(self, db_resource_path, db_source_path, db_target_path, dbs_path):
        """To open the databases as cursor, ready for select, insert, update..."""
        self.dbs_path = dbs_path
        # source database
        self.db_source = self.dbs_path + db_source_path
        self.conn_source = sqlite3.connect(self.db_source)
        self.c_source = self.conn_source.cursor()
        # target database
        self.db_target = self.dbs_path + db_target_path
        self.conn_target = sqlite3.connect(self.db_target)
        self.c_target = self.conn_target.cursor()
        # resource database
        self.db_resource = self.dbs_path + db_resource_path
        self.conn_resource = sqlite3.connect(self.db_resource)
        self.c_resource = self.conn_resource.cursor()

    def create_table(self):
        """To create a table saving post data"""
        sql = 'create table post(platform text, post_type text, coursename text, session text, forumname text, content_text text)'
        self.c_target.execute('DROP TABLE IF EXISTS post')
        self.c_target.execute(sql)

    def select_all_courses(self):
        """To select all courses from database.

        :return: a dictionary of courseid with coursename.
        """
        course_list = dict()
        sql = 'select distinct(courseid), coursename from forum;'
        rows = self.c_source.execute(sql).fetchall()
        if len(rows) != 0:
            for row in rows:
                course_list[row[0]] = row[1]
            return course_list
        else:
            return 0

    def select_all_forums(self, courseid):
        """To select all the forums for each course

        :param courseid: courseid
        :return: a dictionary of forum ids with forum name.
        """
        forum_dict = dict()
        # sql = 'select distinct(id), forumname from forum where courseid = (?)', (courseid)
        # print sql
        rows = self.c_source.execute('select distinct(id), forumname from forum where courseid = (?)', (courseid, )).fetchall()
        if len(rows) != 0:
            for row in rows:
                forum_dict[row[0]] = row[1]
            return forum_dict
        else:
            return 0

    def select_all_threads(self, forumid):
        """To select all the threads for each forum.

        :param forumid: forumid
        :return: a dictionary of threads for each forum with title.
        """
        thread_dict = dict()
        # sql = 'select distinct(id), title from thread where forumid = (?)', (forumid, )
        rows = self.c_source.execute('select distinct(id), title from thread where forumid = (?)', (forumid, )).fetchall()
        if len(rows) != 0:
            for row in rows:
                thread_id = row[0]
                thread_title = row[1]
                thread_dict[thread_id] = thread_title
            return thread_dict
        else:
            return 0

    def select_all_posts(self, threadid):
        """To select all the threads for each forum.

        :param threadid: threadid.
        :return: a dictionary of posts for each thread with post_text.
        """
        post_dict = dict()
        # sql = 'select distinct(id), post_text from post where threadid = (?)', (threadid, )
        rows = self.c_source.execute('select distinct(id), post_text from post where thread_id = (?)', (threadid, )).fetchall()
        if len(rows) != 0:
            for row in rows:
                post_id = row[0]
                post_text = row[1]
                post_dict[post_id] = post_text
            return post_dict
        else:
            return 0

    def select_all_comments(self, postid):
        """To select all comments for each post.

        :param postid: post_id
        :return: a dictionary of comments for each post with comment text.
        """
        comment_dict = dict()
        # sql = 'select distinct(id), comment_text from comment where post_id = (?)', (postid, )
        rows = self.c_source.execute('select distinct(id), comment_text from comment where post_id = (?)', (postid, )).fetchall()
        if len(rows) != 0:
            for row in rows:
                comment_dict[row[0]] = row[1]
            return comment_dict
        else:
            return 0

    def select_instructor_for_course(self, courseid):
        """To select instructor(s) for each course.

        :param courseid: courseid
        :return: a list of instructor name(s) for each course
        """
        instructor_list = []
        # sql =
        rows = self.c_source.execute("select distinct(full_name) from user where user_title = 'Instructor'").fetchall()
        if len(rows) != 0:
            for row in rows:
                instructor_list.append(row[0])
            return instructor_list
        else:
            return 0

    def select_session_for_course(self, courseid):
        """

        :param courseid:
        :return:
        """
        rows = self.c_resource.execute('select startedAt from session where courseId = (?)', (courseid,)).fetchall()
        if len(rows) != 0:
            for row in rows:
                session_course = row[0]
                return session_course
        else:
            print "This course has no session data in our database."
            return 0

    def insert_into_tables(self, platform, post_type ,coursename, session, forumname, text):
        """To insert key components of posts.

        :param platform:
        :param coursename:
        :param forumname:
        :param text:
        :return: 1
        """

        try:
            self.c_target.execute('insert or ignore into post values (?, ?,?,?,?,?)',(platform, post_type, coursename, session, forumname, text, ))
            return 1
        except Exception as e:
            print e
            return 0

    def main(self):
        """Workflow"""
        self.create_table()
        courses = self.select_all_courses()
        for course in courses.iterkeys():
            course_id = course
            course_name = courses[course_id]
            print course_name
            course_session = self.select_session_for_course(courseid=course_id)
            instructors = self.select_instructor_for_course(courseid=course_id)
            forums = self.select_all_forums(courseid=course_id)
            for forum in forums.iterkeys():
                forum_id = forum
                forum_name = forums[forum_id]
                threads = self.select_all_threads(forumid=forum_id)
                if threads != 0:
                    for thread in threads.iterkeys():
                        thread_id = thread
                        thread_title = threads[thread_id]
                        self.insert_into_tables('Coursera', 'Thread', course_name, course_session, forum_name, thread_title)
                        posts = self.select_all_posts(threadid=thread_id)
                        if posts != 0:
                            for post in posts.iterkeys():
                                post_id = post
                                post_text = posts[post_id]
                                self.insert_into_tables('Coursera', 'Post', course_name, course_session, forum_name, post_text)
                                comments = self.select_all_comments(postid=post_id)
                                if comments != 0:
                                    for comment in comments.iterkeys():
                                        comment_text = comments[comment]
                                        self.insert_into_tables('Coursera', 'Comment', course_name, course_session, forum_name, comment_text)
            self.conn_source.commit()
            self.conn_target.commit()
        return 1


class FTSResolver(object):
    """This class is used for full text index for resolving the standard url searching.

    """

    def __init__(self, db_source_path):
        """

        :param db_source_path:
        """
        self.db = db_source_path
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row

    def exe_sql(self, sql):
        """

        :param sql: Sql语句
        :return:
        """
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()

    def select_sql(self, sql, params=None):
        """

        :param sql:
        :param params:
        :return:
        """
        c = self.conn.cursor()
        if params:
            c.execute(sql, params)
        else:
            c.execute(sql)
        return c.fetchall()

    def search_using_like(self, input):
        """
        :param input:
        :return:
        """
        # SEARCH_LIKE = """
        # SELECT courseNameSlug, itemId, `name`, typeName  FROM resource_item WHERE typeName LIKE :typeName AND `name` LIKE :name
        # ORDER BY `name`
        # """
        # for row in selectSql(SEARCH_LIKE, dict(typeName='lecture', name= '1.0')):
        #     print row
        pass

    def search_using_fts4(self, input_string):
        """Full index searching

        :param input_string:
        :return:
        """
        sql_fts4 = """DROP TABLE IF EXISTS resource_index"""
        self.exe_sql(sql_fts4)
        sql_fts4_2 = """CREATE VIRTUAL TABLE resource_index USING fts4(itemId text, content)"""
        self.exe_sql(sql_fts4_2)

        sql_populate_index = """INSERT INTO resource_index (itemId, content)
                              SELECT itemId,standard_url FROM resource"""
        self.exe_sql(sql_populate_index)
        search_fts4 = """SELECT standard_url  FROM resource WHERE itemId IN (
                         SELECT itemId FROM resource_index WHERE content MATCH :Content)"""
        search_result = []
        if len(input_string) != 0:
            for row in self.select_sql(search_fts4, dict(Content=input_string)):
                search_result.append(row)
        elif len(input_string) >= 2:
            print "Please input only one short form url"
        else:
            print "Please check the short form url."
        self.exe_sql(sql_fts4)
        return search_result


class MURI(FTSResolver):
    """This class is used for presenting a typical example for MURI(MOOC Unique Resource Identifier) system.

    Including mention extraction, short form URL generation, standard URL generation and the last step of actual URL generation.
    Dataflow is from source post, to short form URL, to standard URL and actual URL for the post.

    Directory and subdirectories.
        General Dir
            -Platform
                -Coursename
                    -ForumName
                        -post1
                        -post2
                        -...
                        -postN
    The format of each post:
        Line1: post_content
        Line2: mention1, short_form, standard_form, resolved_url;
        ...
        LineN: mentionN, short_form, standard_form, resolved_url.

    Steps:
        Step1: Select post from postdata.db including platform, coursename, forumname, content_text;
        Step2: Processing one post
        Step3: Do the four steps for each automatically procedures.

    """

    def __init__(self, post_db_path, resource_db_path, dbs_path):
        """To initialize the post_db_path and resource_db_path for matching.

        :param post_db_path: postdata.db
        :param resource_db_path: MOOCDB.db
        :param dbs_path: 'C:/Users/anyah/OneDrive/Wikifier-master/Wikifier-master/server-master/'
        """
        self.post_db_path = dbs_path + post_db_path
        self.resource_db_path = dbs_path + resource_db_path
        # post database
        self.conn_post = sqlite3.connect(self.post_db_path)
        self.c_post = self.conn_post.cursor()
        # resource database
        self.conn_resource = sqlite3.connect(self.resource_db_path)
        self.c_resource = self.conn_resource.cursor()

    @staticmethod
    def match_key_words(reg_exp, post_content):
        """Matching using reg_exp.

        :param reg_exp:
        :param post_content: The source post
        :return: a list of matches or 0
        """
        matches = re.findall(reg_exp, post_content.lower())
        if len(matches) != 0:
            return matches
        else:
            return 0

    def mention_extraction(self, post_text, reg_exp):
        """Return a list of mentions in the post_text

        :param post_text:
        :param reg_exp: regular expression rule for extracting mentions that meets the requirement.
        :return: a list of mentions or 0
        """
        matches = self.match_key_words(reg_exp=reg_exp, post_content=post_text)
        if matches != 0:
            return matches
        else:
            return 0

    @staticmethod
    def short_form_generation(match, prefix, coursename, session, forumname):
        """Generate short form for one mention
        The structure of the short form is:
            prefix + coursename + session + forumname + mention_type + mention_id

        :param match:
        :param prefix:
        :return: short form URL for the input mention with the designed prefix
        """
        if len(match) == 4:
            if match[1] in ['exam']:
                url = prefix + '/' + coursename + '/' + session + '/' + forumname + '/' + 'exam' + '/' + match[3]
                return url
            elif match[1] in ['quiz', 'problem', 'question']:
                url = prefix + '/' + coursename + '/' + session + '/' + forumname + '/' + 'quiz' + '/' + match[3]
                return url
            elif match[1] in ['module', 'lecture', 'video']:
                url = prefix + '/' + coursename + '/' + session + '/' + forumname + '/' + 'lecture' + '/' + match[3]
                return url
            elif match[1] in ['slide']:
                url = prefix + '/' + coursename + '/' + session + '/' + forumname + '/' + 'supplement' + '/' + match[3]
                return url
            else:
                print "Sorry, this type of mention can not be solved by our system."
                return 0
        elif len(match) == 3:
            if match[1] in ['exam']:
                url = prefix + '/' + coursename + '/' + session + '/' + forumname + '/' + 'exam' + '/' + match[2]
                return url
            elif match[1] in ['quiz', 'problem', 'question']:
                url = prefix + '/' + coursename + '/' + session + '/' + forumname + '/' + 'quiz' + '/' + match[2]
                return url
            elif match[1] in ['module', 'lecture', 'video']:
                url = prefix + '/' + coursename + '/' + session + '/' + forumname + '/' + 'lecture' + '/' + match[2]
                return url
            elif match[1] in ['slide']:
                url = prefix + '/' + coursename + '/' + session + '/' + forumname + '/' + 'supplement' + '/' + match[2]
                return url
            else:
                print "Sorry, this type of mention can not be solved by our system."
                return 0

    def standard_form_search(self, short_form):  #full text search
        """Standard form is automatically generated by our system.
        The information are from two directions:
            short_form: coursename, session, forumname(week number),

        #Step 1: Select the resource from the resource_database
        #Step 2: Generate the standard form URL for this resource.

        :param short_form: short form of mention.
        :return: standard_URL
        """
        line_str = short_form.split('/')
        coursename, session, forumname, resourcetype,resource_loc = line_str[3], line_str[4], line_str[5], line_str[6], line_str[7]
        input_str = coursename + ' ' + session + ' ' + resourcetype + ' ' + resource_loc
        print input_str
        fts_resolver = FTSResolver(self.resource_db_path)
        search_result = fts_resolver.search_using_fts4(input_string=input_str)
        if len(search_result) == 1:
            return search_result[0][0]
        elif len(search_result) == 0:
            return 'NULL'
        else:
            return search_result[0][0]  # 如果出现多于一个的结果，返回结果列表的第一个

    def actual_url_lookup(self, standard_url):
        """The only input is standard_url.

        :param standard_url:
        :return: actual URL
        """
        rows = self.c_resource.execute('select actual_url from resource where standard_url = (?)', (standard_url,)).fetchall()
        if len(rows) == 0:
            print "No actual URL for this resource."
            return 0
        elif len(rows) == 1:
            actual_url = rows[0][0]
            return actual_url
        else:  # len>1
            # HOW TO CHOOSE THE MOST APPROPRIATE ONE.
            for row in rows:
                actual_url = row[0]
                return actual_url

    @staticmethod
    def mkdir(path):
        """mkdir for a path

        :param path:
        :return:
        """
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True

    def main(self, root_path, reg_exp, short_form_prefix):
        """Only considering Week discussions of all the resources.

        :return:
        """
        self.c_post.execute("select * from post where forumname like 'Week%'")
        row = self.c_post.fetchone()
        count = 0
        while row is not None:
            count += 1
            print count
            platform, post_type, coursename, session, forumname, post_text = row[0], row[1], row[2], row[3], row[4], \
                                                                             row[5]
            new_path = root_path + '/' + platform + '/' + coursename + '/' + session + '/' + forumname + '/'
            self.mkdir(new_path)
            new_str = post_text + '\n'
            mentions_list = self.mention_extraction(post_text=post_text, reg_exp=reg_exp)
            if mentions_list != 0:
                # only save the posts have mentions with 'YES'
                file_open = open(new_path + 'post' + '_' + str(count) + '_' + 'YES' + '.txt', 'w')
                for mention in mentions_list:
                    short_form = self.short_form_generation(match=mention, prefix=short_form_prefix, coursename=coursename, session=session, forumname=forumname)
                    if short_form != 0:
                        standard_form = self.standard_form_search(short_form=short_form)  # remember the sessionId
                        if standard_form is not 'NULL':
                            print mention, standard_form
                            actual_url = self.actual_url_lookup(standard_url=standard_form)
                            if actual_url != 0:
                                new_str += mention[0] + '||' + short_form + '||' + standard_form + '||' + actual_url + '\n'
                            else:
                                new_str += mention[0] + '||' + short_form + '||' + standard_form + '\n'
                        else:
                            new_str += mention[0] + '||' + short_form + '\n'
                    else:
                        new_str += mention[0] + '\n'
                    file_open.write(new_str.encode('utf-8'))
                file_open.close()
            else:
                # save the post without mention with 'NO'
                file_open = open(new_path + 'post' + '_' + str(count) + '_' + 'NO' + '.txt', 'w')
                file_open.write(new_str.encode('utf-8'))
                file_open.close()
            row = self.c_post.fetchone()

# if __name__ == '__main__':
#     dbs_path = 'C:/Users/anyah/OneDrive/Wikifier-master/Wikifier-master/server-master/'
#     database_source = 'nusdata.db'
#     database_target = 'postdata.db'
#     database_resource = 'MOOCDB.db'
#     sql_actions = CreatePostTable(dbs_path=dbs_path, db_source_path=database_source, db_target_path=database_target, db_resource_path=database_resource)
#     a = sql_actions.main()
#     if a == 1:
#         print 'Finished!'


if __name__ == '__main__':
    dbs_path = 'C:/Users/anyah/OneDrive/Wikifier-master/Wikifier-master/server-master/'
    post_db_path = 'postdata.db'
    resource_db_path = 'MOOCDB.db'
    muri_instance = MURI(dbs_path=dbs_path, post_db_path=post_db_path, resource_db_path=resource_db_path)
    root_path = 'C:/Users/anyah/OneDrive/Wikifier-master/Wikifier-master/result_data'
    reg_exp = "(([Pp]roblem|[Qq]uiz*|[Qq]uestion|[Mm]odule|[Ll]ecture|[Ss]lide|[Vv]ideo|[Hh]omework)( *[#]*)( *[0-9]+ *?[\.-]? *?[0-9]*)(?![0-9]*%))"
    short_forum_prefix = 'http://www.wing.comp.nus.edu.sg'
    muri_instance.main(root_path=root_path, reg_exp=reg_exp, short_form_prefix=short_forum_prefix)
    muri_instance.conn_post.close()
    muri_instance.conn_resource.close()



