# Generated by Django 4.0 on 2021-12-29 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksAuthor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('birth_year', models.SmallIntegerField(blank=True, null=True)),
                ('death_year', models.SmallIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'books_author',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksBook',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('download_count', models.IntegerField(blank=True, null=True)),
                ('gutenberg_id', models.IntegerField()),
                ('media_type', models.CharField(max_length=16)),
                ('title', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'books_book',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksBookAuthors',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('author_id', models.IntegerField()),
            ],
            options={
                'db_table': 'books_book_authors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksBookBookshelves',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('bookshelf_id', models.IntegerField()),
            ],
            options={
                'db_table': 'books_book_bookshelves',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksBookLanguages',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('language_id', models.IntegerField()),
            ],
            options={
                'db_table': 'books_book_languages',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksBookshelf',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'books_bookshelf',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksBookSubjects',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('subject_id', models.IntegerField()),
            ],
            options={
                'db_table': 'books_book_subjects',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksFormat',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('mime_type', models.CharField(max_length=32)),
                ('url', models.TextField()),
                ('book_id', models.IntegerField()),
            ],
            options={
                'db_table': 'books_format',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksLanguage',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'books_language',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksSubject',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'books_subject',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
    ]
