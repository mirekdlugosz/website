Title: Django: data modified in pre_save signal is not saved
Slug: django-data-modified-in-pre-save-signal-is-not-saved
Date: 2025-03-12 19:09:14
Category: Blog
Tags: Python, planet AST, planet MoT, planet Python, tutorial

When I was working on my first Django project, I encountered a problem where modifications done inside [`pre_save` signal](https://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.pre_save) were not stored in the database. Back then it took me a couple of hours to figure out what is wrong and how to fix it. I'm sharing what I've learned to save that time someone else.

Imagine the application to track your gym workouts. At the core of application is exercise session, which knows how many repetitions you want to do and how many you have done so far. Once you do enough repetitions, session is considered complete. It could be implemented like that:

```python
class ExerciseSession(models.Model):
    target_repetitions = models.IntegerField(null=False, blank=False)
    repetitions = models.IntegerField(null=False, blank=False, default=0)
    completed = models.BooleanField(null=False, blank=False, default=False)
```

Since "session is complete once you do enough repetitions" is a hard rule, it needs to be enforced. `pre_save` signal sounds like reasonable place to implement it, as it allows us to have many functions that modify `repetitions`. Signal handler might look like that:

```python
@receiver(pre_save, sender=models.ExerciseSession)
def exercise_session_pre_save(sender, instance, raw, using, update_fields, **kwargs):
    if instance.repetitions >= instance.target_repetitions:
        instance.completed = True
```

With the above setup we can modify the model instance and rest assured that exercise session is marked as completed when needed:

```python
exercise_session.repetitions = 10
exercise_session.save(update_fields=["repetitions"])
```

Except that... this doesn't work. Once you retrieve this exercise session from database, `completed` will be set to False.

The reason for this is at intersection of `pre_save` signal and `update_fields` argument. `pre_save` is called early in `save()` call and may be used to modify the instance before data is saved in database. However, SQL query constructed later in `save()` call will contain only the fields listed in `update_fields` argument.

So when calling a `save()`, you need to predict that `pre_save` signal might modify the instance, and include possibly modified fields in `update_fields` list:

```python
exercise_session.save(update_fields=["repetitions", "completed"])
```

The complete code used in this blog post is available in [GitHub repository](https://github.com/mirekdlugosz/django-pre-save-issue-demo). See the `README` file for instructions how to set up and run the project.
