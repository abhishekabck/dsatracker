from django.db import models
from django.contrib.postgres.search import TrigramSimilarity


# Create your models here.
class DSATopics(models.Model):
    topic_name = models.CharField(max_length=200)
    s_question = None

    def patterns(self):
        if self.id:
            query_object = DSAPattern.objects.filter(topic_id=self.id)
            if self.s_question:
                query_object = query_object.annotate(
                    similarity=TrigramSimilarity("dsapatternquestions__question_heading", self.s_question)
                ).filter(similarity__gte=0.1).order_by("id", "-similarity").distinct("id")
            return query_object

    def __str__(self):
        return f"Question Id:{self.id} Question Name:{self.topic_name}"


class DSAPattern(models.Model):
    topic = models.ForeignKey(DSATopics, on_delete=models.RESTRICT)
    pattern_name = models.CharField(max_length=200)
    s_question = None

    def questions(self):
        if self.id:
            query_object = DSAPatternQuestions.objects.filter(pattern_id=self.id)
            if self.s_question:  # search question
                query_object = query_object.annotate(
                    similarity=TrigramSimilarity("question_heading", self.s_question)
                ).filter(similarity__gte=0.1).order_by("id", "-similarity").distinct("id")
            return query_object


class DSAPatternQuestions(models.Model):
    pattern = models.ForeignKey(DSAPattern, on_delete=models.RESTRICT)
    question_heading = models.CharField(max_length=1000)
    question_URL = models.URLField(null=True, blank=True)
    solved = models.BooleanField(default=False)
    solved_date = models.DateTimeField(null=True, blank=True)

    def have_url(self):
        return self.question_URL != None

