from django.db import models

class User(models.Model):
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  phone = models.CharField(max_length=200)
  address = models.CharField(max_length=200)

class Domain(models.Model):
  name = models.CharField(max_length=200)

class Website(models.Model):
  name = models.CharField(max_length=200)
  users = models.ForeignKey(User)
  domains = models.ForeignKey(Domain)
  enabled = models.BooleanField()
  php_enabled = models.BooleanField()
  cgi_enabled = models.BooleanField()
  wsgi_enabled = models.BooleanField()
