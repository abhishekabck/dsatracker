from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.postgres.search import TrigramSimilarity
from .models import *
import json


# """
# used to use dsaquestions.csv file for questions and patterns
# def dsaTracker1(request):
#     import pandas as pd
#     data = pd.read_csv(r"C:\Users\abhis\PycharmProjects\Django_learning\firstproject\dsaTracker\dsaquestions.csv")
#     bool_idx = data[data.columns[1]].isnull()
#     topics = data[bool_idx]
#     pattern = dict()
#     topics = list(map(lambda x: x.split(sep='.', maxsplit=1)[-1].strip(), topics[data.columns[0]].tolist()))
#     key = None
#     idx = -1
#     for i in range(data.shape[0]):
#         if bool_idx[i]:
#             idx += 1
#             pattern[topics[idx]] = list()
#             key = DSATopics.objects.filter(topic_name=topics[idx]).first()
#         else:
#             content = data.iloc[i, 0].split(":", maxsplit=1)[-1].strip()
#             questions = [d.split('.', 1)[-1].strip() for d in data.iloc[i, 1].split(",")]
#             pattern[topics[idx]].append({content: questions})
#             p = DSAPattern(topic=key, pattern_name=content)
#             p.save()
#             qs = []
#             for q in questions:
#                 qs.append(DSAPatternQuestions(pattern=p, question_heading=q))
#             DSAPatternQuestions.objects.bulk_create(qs)
#
#     return render(request, "dsaTracker.html", {"topics": pattern})
# """

def index(request):
    context = {
        'topics': DSATopics.objects.all(),
        'total_questions': DSAPatternQuestions.objects.count(),
        'total_solved': DSAPatternQuestions.objects.filter(solved=True).count(),
    }
    if request.method == "POST":
        question = request.POST.get("search_question")
        if question:
            print("Search Topics:-", question)
            DSAPattern.s_question = question
            DSATopics.s_question = question
            context["topics"] = DSATopics.objects.annotate(
                similarity=TrigramSimilarity("dsapattern__dsapatternquestions__question_heading", question)
            ).filter(similarity__gte=0.3).order_by("id", "-similarity").distinct("id")
        else:
            DSAPattern.s_question = None
            DSATopics.s_question = None
    else:
        DSAPattern.s_question = None
        DSATopics.s_question = None
        question = ""

    context["total_unsolved"] = context["total_questions"] - context["total_solved"]
    context["search_question"] = question
    context["topics_length"] = len(context["topics"])
    return render(request, "dashboard.html", context)


@require_http_methods(["PUT"])
def update_status(request, id):
    # Django doesn't parse PUT data into request.POST by default
    # You need to access request.body and decode JSON or form data
    data = json.loads(request.body.decode("utf-8"))

    solved = str(data.get("status")).lower() == "true"
    question = get_object_or_404(DSAPatternQuestions, id=id)
    question.solved = solved
    question.save()
    return JsonResponse({"message": "Status updated", "id": question.id, "solved": question.solved})


@require_http_methods(["PUT"])
def update_url(request, id):
    url = json.loads(request.body.decode("utf-8")).get("url")
    question = get_object_or_404(DSAPatternQuestions, id=id)
    question.question_URL = url
    question.save()
    return JsonResponse({"message": "URL updated", "id": question.id, "url": question.question_URL})