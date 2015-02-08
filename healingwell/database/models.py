import peewee as pw

db = pw.PostgresqlDatabase(None, autorollback=True) # path to be specified at runtime


#------------------------------
# base model to subclass from
#------------------------------

class BaseModel(pw.Model):
    class Meta:
        database = db

#------------------------------
# models for healingwell text analytics
#------------------------------

class Post(BaseModel):
    page_url = pw.CharField(max_length=100)

    post_url = pw.CharField(max_length=100, unique=True)
    post_author = pw.CharField(max_length=50)
    post_author_url = pw.CharField(max_length=100)
    post_author_rank = pw.CharField(max_length=30)
    post_date = pw.DateTimeField()
    post_content = pw.TextField()

    thread_url = pw.CharField(max_length=100)
    thread_title = pw.CharField(max_length=150)

    section_url = pw.CharField(max_length=100)
    section_title = pw.CharField(max_length=50)
