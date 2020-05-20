from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
	title = StringField("Заговолок статьи")
	body = TextAreaField("Текст")
