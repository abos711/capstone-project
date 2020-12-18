from  django.db import models

class Activity(models.Model):
  # Title will be diaper change, bottle, nap
    activity = models.CharField(max_length=100)
    # Description of title (i.e. pee, poop, breast milk, formula, etc)
    description = models.CharField(max_length=100)
    # add note here
    note = models.CharField(max_length=100)
    parent_id = models.ForeignKey('Parent', related_name='activities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Emmy had a {self.activity} at {self.created_at}"

    def as_dict(self):
  # return it as a dictionary
    return {
        'id': self.id,
        'activity': self.activity,
        'description': self.description,
        'note': self.note,
        'created_at': self.created_at,
        'updated_at': self.updated_at
    }
