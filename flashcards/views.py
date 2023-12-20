from django.shortcuts import render, redirect, HttpResponse
from .models import FlashCard, Room, Message
from .forms import FlashCardForm
import random
import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
key="AIzaSyAZ8ri4gSLDLKlfbqqDPWiiKROp2d-xAX8"


import google.generativeai as palm

#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

# -------------------------------------------------------------------------------

# get number of cards in evey category
def get_counts(all_cards):
    counts = []
    count_alg = all_cards.filter(category='Algorithms').count()
    counts.append(count_alg)
    count_ds = all_cards.filter(category='OS').count()
    counts.append(count_ds)
    count_com = all_cards.filter(category='DBMS').count()
    counts.append(count_com)
    return counts

# get n popular/most liked cards
def get_popular_cards(all_cards, n):
    popular_cards = all_cards.order_by('likes')[:n]
    return popular_cards


@login_required
def ask_AI(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'counts':counts, 'popular_cards':popular_cards }
    return render(request,'flashcards/ask_AI.html',context )
    

def generate(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]

    question=""
    if request.method=="POST":
        question=request.POST['question']
        pass
    
    if question=="":
        answer="ask a question"

    else:
        
        palm.configure(api_key=key)
        response = palm.generate_text(prompt=question)
        answer= response.result
        
    answer_html = answer.replace('\n', '<br>')

    context={'result':answer_html,'counts':counts, 'popular_cards':popular_cards,"question":question}
    return render(request, 'flashcards/generate.html', context)

    



@login_required
def chat_home(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/chat_home.html',context)

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room) 
    return render(request, 'flashcards/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.user.username

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def home(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    #cards = sorted(all_cards.order_by('front'), key=lambda x: random.random())
    paginator = Paginator(all_cards, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]

    context = {'page_obj':page_obj, 'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/home.html', context)


def get_cards_by_category(request, category):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    cards = all_cards.filter(category=category)
    paginator = Paginator(cards, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'page_obj':page_obj, 'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/home.html', context)

# add flashcard
@login_required
def add_card(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    if request.method == 'POST':
        form = FlashCardForm(request.POST)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.creator = request.user
            new_card.save()
            messages.success(request, f'Flashcard added!')
            return redirect('home')
    else:
        form = FlashCardForm()

    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'form':form, 'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/add_card.html', context)


# edit card
@login_required
def edit_card(request, id):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    card = FlashCard.objects.get(id=id)
    if request.method == 'POST':
        form = FlashCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, f'Flashcard updated!')
            return redirect('home')
    else:
        form = FlashCardForm(instance=card)

    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'form':form, 'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/edit_card.html', context)


# search keywords - top 20 results
def search_keywords(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    cards = FlashCard.objects.filter(front__contains=request.GET.get('keywords'))[:20]
    paginator = Paginator(cards, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'page_obj': page_obj, 'counts':counts, 'popular_cards':popular_cards}
    return render(request, 'flashcards/home.html', context)


# learn with flashcards
def learn(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    cards = all_cards.filter(known=0)
    cards = sorted(cards.order_by('likes'), key=lambda x: random.random())
    context = {'card': cards[0]}
    return render(request, 'flashcards/learn.html', context)


# mark a card as known
@login_required
def mark_known(request, id):
    card = FlashCard.objects.get(id=id)
    card.known = 1
    card.save()
    return redirect('learn')


# liking a card
def mark_liked(request, id):
    card = FlashCard.objects.get(id=id)
    card.likes += 1
    card.save()
    return redirect('home')


# save and export cards as csv file
def dump_csv(request):
    cards = FlashCard.objects.all()
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)
    response['Content-Disposition'] = 'attachment; filename="flashcards.csv"'
    fieldnames = ['ID', 'Category', 'Front', 'Back', 'Creator', 'Likes', 'Known']
    writer.writerow(fieldnames)
    output = []
    for card in cards:
            output.append([card.id, card.category, card.front, card.back, card.creator, card.likes, card.known])
    writer.writerows(output)
    # with open('flashcards.csv', 'w', newline='') as file:
    #     fieldnames = ['ID', 'Category', 'Front', 'Back', 'Creator', 'Likes', 'Known']
    #     writer = csv.writer(file)
    #     writer.writerow(fieldnames)
    #     for card in cards:
    #         output.append([card.id, card.category, card.front, card.back, card.creator, card.likes, card.known])
    #     writer.writerows(output)
    return response





