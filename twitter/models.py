from django.db import models

# Create your models here.
class APIKeys(models.Model):

    api_key = models.CharField(max_length=100)
    api_secret_key = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    access_token_secret = models.CharField(max_length=100)


class SearchLog(models.Model):
    term = models.CharField(max_length=100, blank=False, null=True)
    total_tweet = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['term'], name='new_constraint1')
        ]
    def __str__(self):
        return self.term


class Twitter(models.Model):
    term = models.CharField(max_length=100)
    twitterid = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField()
    text = models.CharField(max_length=500, null=True)
    sentimentscore = models.DecimalField(max_digits=10, decimal_places=2)
    cleaned_text = models.CharField(max_length=500, null=True)
    hastags = models.CharField(max_length=500, null=True)
    screenname = models.CharField(max_length=100, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['twitterid'], name='new_constraint')
        ]
    def __str__(self):
        return self.text



    def __str__(self):
        return self.term