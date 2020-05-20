from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from models import Post, Tag
from .forms import PostForm
from app import db
import datetime
from flask_security import login_required


posts = Blueprint('posts', __name__, template_folder='templates')

MONTHS = {'01': 'Январь',
		  '02': 'Февраль',
		  '03': 'Март',
		  '04': 'Апрель',
		  '05': 'Май',
		  '06': 'Июнь',
		  '07': 'Июль',
		  '08': 'Август',
		  '09': 'Сентябрь',
		  '10': 'Октябрь',
		  '11': 'Ноябрь',
		  '12': 'Декабрь'}

START_YEAR = 2020


def get_date():
	cur_date = str(datetime.datetime.now())[:7].split('-')
	cur_month = cur_date[1]
	cur_year = int(cur_date[0])
	current_date = f'{cur_year}-{cur_month}'

	return cur_year, cur_month, current_date


def list_archive(cur_year, cur_month, current_date):

	posts = Post.query

	result_archive = []

	while START_YEAR <= cur_year:

		for month in sorted(MONTHS.keys(), reverse=True):
			date_string = f'{cur_year}-{month}'
			if date_string != current_date:
				if posts.filter(Post.created.contains(date_string)).all():
					result_archive.append((str(cur_year), month, MONTHS[month]))

		cur_year -= 1

	return result_archive


@posts.route('/create', methods=["POST", "GET"])
@login_required
def create_post():
	if request.method == "POST":
		title = request.form['title']
		body = request.form['body']
		try:
			post = Post(title=title, body=body)
			db.session.add(post)
			db.session.commit()
		except:
			print("Не получилось записать новый пост в базу данных")
		return redirect(url_for('posts.index'))

	form = PostForm()
	return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
	post = Post.query.filter(Post.slug == slug).first_or_404()

	if request.method == 'POST':
		form = PostForm(formdata=request.form, obj=post)
		form.populate_obj(post)
		db.session.commit()

		return redirect(url_for('posts.post_detail', slug=post.slug))

	form = PostForm(obj=post)
	return render_template('posts/edit_post.html', post=post, form=form)


@posts.route('/posts/<slug>/delete')
@login_required
def delete_post(slug):
	post = Post.query.filter(Post.slug == slug).first_or_404()
	try:
		db.session.delete(post)
		db.session.commit()
	except:
		print("Не получилось удалить пост из базы данных")
	return redirect(url_for('posts.index'))


@posts.route('/')
def index():

	cur_year, cur_month, current_date = get_date()

	s = request.args.get('s')
	if s:
		posts = Post.query.filter(Post.title.contains(s) | Post.body.contains(s)).all()
	else:
		posts = Post.query.filter(Post.created.contains(current_date)).all()[::-1]

	tags_all = Tag.query.all()
	return render_template('posts/index.html',
						   posts=posts,
						   tags_all=tags_all,
						   result_archive=list_archive(cur_year, cur_month, current_date))


#@posts.route('')

@posts.route('/<slug>')
def post_detail(slug):
	post = Post.query.filter(Post.slug==slug).first_or_404()
	tags = post.tags
	result_archive = list_archive(*get_date())
	try:
		post_pre = Post.query.filter(Post.id == post.id - 1).first()
	except:
		post_pre = None
	try:
		post_next = Post.query.filter(Post.id == post.id + 1).first()
	except:
		post_next = None
	posts = Post.query.all()[::-1][:4]
	tags_all = Tag.query.all()
	return render_template('posts/post_detail.html',
						    post=post,
						    post_pre=post_pre,
						    post_next=post_next,
						    posts=posts,
						    tags=tags,
						    tags_all=tags_all,
						   result_archive=result_archive)


@posts.route('/tag/<slug>')
def tag_detail(slug):
	tag = Tag.query.filter(Tag.slug==slug).first_or_404()
	posts = tag.posts.all()
	posts_recent = Post.query.all()[::-1][:4]
	tags_all = Tag.query.all()
	result_archive = list_archive(*get_date())
	return render_template('posts/tag_detail.html', tag=tag, posts=posts,
						   posts_recent=posts_recent, tags_all=tags_all,
						   result_archive=result_archive)


@posts.route('/<year>/<month>')
def archive_detail(year, month):
	last_date = f'{year}-{month}'
	archive_posts = Post.query.filter(Post.created.contains(last_date)).order_by(Post.created.desc()).all()
	tags_all = Tag.query.all()
	result_archive = list_archive(*get_date())
	recent_posts = Post.query.all()[::-1][:4]

	return render_template('posts/archive_detail.html',
						   archive_posts=archive_posts,
						   month_name=MONTHS[month],
						   year=year,
						   tags_all=tags_all,
						   result_archive=result_archive,
						   recent_posts=recent_posts)
