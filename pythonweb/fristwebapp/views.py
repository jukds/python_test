from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
from bs4 import BeautifulSoup
import requests

# Create your views here.
#重构
def check_topic_owner(topic,request):
    if topic.owner != request.user:
        raise Http404

def get_weather(url):
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'html')
    conMidtab = soup.find('div', class_='conMidtab')
    conMidtab2_list = conMidtab.find_all('div', class_='conMidtab2')
    info = ''
    for conMidtab2 in conMidtab2_list:
        tr_list = conMidtab2.find_all('tr')[2:]
        for index, tr in enumerate(tr_list):
            if index == 0:
                td = tr.find_all('td')
                provence = td[0].text.replace('\n', '')
                city = td[1].text.replace('\n', '')
                night_weather = td[5].text.replace('\n', '')
                min_temperature = td[7].text.replace('\n', '')
            else:
                td = tr.find_all('td')
                city = td[0].text.replace('\n', '')
                night_weather = td[4].text.replace('\n', '')
                min_temperature = td[6].text.replace('\n', '')
                    
            # print('%s 夜晚天气：%s，最低气温: %s' % (provence+city, night_weather, min_temperature))
            info = info + provence+city+"夜晚天气"+ night_weather+"最低气温"+min_temperature+"<br/>"
            # sleep(1)
    return info


def index(request):
    return render(request,'fristwebapp/index.html')

#test

def ajax_page(request):
    return render_to_response('fristwebapp/ajax.html')

def ajax_test(request):
    return HttpResponse('hello nihao!woaini!')

@csrf_exempt  
def ajax_test2(request):
    name = request.POST['name']
    pwd = request.POST['pwd'] 
    url = 'http://www.weather.com.cn/textFC/hb.shtml'
    anwser = get_weather(url)
    return HttpResponse(anwser)

@login_required
def topics(request):
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'fristwebapp/topics.html',context)

@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id = topic_id)
    #保护用户主题
    check_topic_owner(topic,request)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    return render(request,'fristwebapp/topic.html',context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else :
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('fristwebapp:topics'))

    context = {'form':form}
    return render(request,'fristwebapp/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    #add new entry in target topic
    topic = Topic.objects.get(id=topic_id)

    if request.method !='POST':
        form = EntryForm()
    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('fristwebapp:topic',args=[topic_id]))
    
    context = {'topic': topic,'form':form}
    return render(request,'fristwebapp/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    #edit entry
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    check_topic_owner(topic,request)
    
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance = entry,data =request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('fristwebapp:topic',args =[topic.id]))
    
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'fristwebapp/edit_entry.html',context)


