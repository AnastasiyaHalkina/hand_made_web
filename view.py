from app import app
from flask import render_template
from models import Post, Tag
from flask import request
import datetime
from posts.blueprint import get_date, list_archive


@app.route('/')
def index():
	tags_all = Tag.query.all()

	cur_year, cur_month, current_date = get_date()

	s = request.args.get('s')
	if s:
		posts = Post.query.filter(Post.title.contains(s) | Post.body.contains(s)).all()
		return render_template('posts/index.html', posts=posts,
							   tags_all=tags_all)
	else:
		posts_all = Post.query.filter(Post.created.contains(current_date)).all()[::-1]

	post_first = posts_all[0]
	posts_recent = posts_all[1:4]

	return render_template('index.html', posts_all=posts_all,
						   post_first=post_first,
						   posts_recent=posts_recent,
						   tags_all=tags_all,
						   result_archive=list_archive(cur_year, cur_month, current_date))


@app.errorhandler(404)
def page_not_found(event):
	return render_template('404.html'), 404
