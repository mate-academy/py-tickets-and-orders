from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ticket',
            name='unique_row_seat_movie_session_constraint',
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='unique_row_seat_movie_session_constraint'),
        ),
    ]
